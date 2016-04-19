from django.db import models
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
import datetime

from simple_history.models import HistoricalRecords


class AbstractNamedItem(models.Model):
    name = models.CharField(max_length=120, verbose_name=_('name'), )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class HistoryURLMixin(object):
    def get_history_url(self):
        return reverse('admin:products_{model_name}_history'.format(model_name=self._meta.model_name), args=[self.pk])


class AbstractTreeItem(models.Model):
    def get_path(self):
        path = []
        current = self

        while current is not None:
            path.append(current)
            current = current.parent if hasattr(current, 'parent') else None

        return reversed(path)

    class Meta:
        abstract = True


class AbstractNamedTreeItem(AbstractNamedItem, AbstractTreeItem):
    class Meta:
        abstract = True


class ChildMetaMixin(object):
    unique_together = ('name', 'parent',)


class Customer(AbstractNamedTreeItem, HistoryURLMixin):
    history = HistoricalRecords()
    invoice = models.CharField(max_length=100, blank=True, )
    total_weight = models.CharField(blank=True, null=True, max_length=256, )
    in_close = models.BooleanField(default=False)
    time_close = models.DateTimeField(default=datetime.datetime.now())
    in_close_time = models.IntegerField(default=0)

    @property
    def is_closed(self):
        closed = self.box_set.filter(is_closed=True).count() == self.box_set.count()
        if closed and not self.in_close:
            self.time_close = datetime.datetime.now()
            self.in_close = True
            self.save()
        elif self.in_close and not closed:
            self.in_close = False
            self.time_close = datetime.datetime.now()
            self.in_close_time = 0
            self.save()
        if self.in_close and self.in_close_time < 31:
            time_now = datetime.datetime.now().date()
            time_close = self.time_close.date()
            delta = (time_now - time_close).days
            if delta != self.in_close_time:
                self.in_close_time = delta
                self.save()
        elif not self.in_close:
            self.in_close_time = 0

        return closed

    def get_absolute_url(self):
        return reverse('box-pallet', kwargs={'customer_pk': self.pk})

    def get_box_url(self):
        return reverse('box-list', kwargs={'customer_pk': self.pk})

    def get_pallet_url(self):
        return reverse('pallet-list', kwargs={'customer_pk': self.pk})

    def get_delete_url(self):
        return reverse('customer-delete', kwargs={'customer_pk': self.pk})

    def get_export_url(self):
        return reverse('customer-export', kwargs={'customer_pk': self.pk})

    class Meta:
        verbose_name = _('customer')
        verbose_name_plural = _('customers')


class Box(AbstractNamedTreeItem, HistoryURLMixin):
    history = HistoricalRecords()
    parent = models.ForeignKey(Customer, related_name='box_set', verbose_name=_('customer'))
    is_closed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('product-list', kwargs={'customer_pk': self.parent.pk, 'box_pk': self.pk})

    def get_delete_url(self):
        return reverse('box-delete', kwargs={'customer_pk': self.parent.pk, 'box_pk': self.pk, })

    def get_export_url(self):
        return reverse('box-export', kwargs={'customer_pk': self.parent.pk, 'box_pk': self.pk, })

    class Meta(ChildMetaMixin):
        verbose_name = _('box')
        verbose_name_plural = _('boxes')


class Product(AbstractNamedItem):
    history = HistoricalRecords()
    barcode = models.CharField(max_length=64, verbose_name=_('barcode'))
    order = models.CharField(max_length=120, verbose_name=_('order'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))

    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')
        unique_together = ('name', 'barcode', 'order',)


class ProductPurchase(AbstractTreeItem, HistoryURLMixin):
    history = HistoricalRecords()
    parent = models.ForeignKey(Box, verbose_name=_('box'))
    product = models.ForeignKey(Product, )
    quantity_override = models.PositiveIntegerField(default=None, null=True, blank=True, verbose_name=_('quantity'))
    order_override = models.CharField(max_length=120, verbose_name=_('order'), blank=True, null=True, )

    def get_delete_url(self):
        return reverse('product-delete', kwargs={'customer_pk': self.parent.parent.pk, 'box_pk': self.parent.pk,
                                                 'productpurchase_pk': self.pk})

    def get_edit_url(self):
        return reverse('product-update', kwargs={'customer_pk': self.parent.parent.pk, 'box_pk': self.parent.pk,
                                                 'productpurchase_pk': self.pk})

    @property
    def name(self):
        return self.product.name

    @property
    def barcode(self):
        return self.product.barcode

    @property
    def order(self):
        return self.product.order if self.order_override is None else self.order_override

    @order.setter
    def order(self, value):
        self.order_override = value

    @property
    def quantity(self):
        return self.product.quantity if self.quantity_override is None else self.quantity_override

    @quantity.setter
    def quantity(self, value):
        self.quantity_override = value

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = _('product purchase')
        verbose_name_plural = _('product purchases')
        unique_together = ('product', 'parent')

class Pallet(AbstractNamedTreeItem, HistoryURLMixin):
    history = HistoricalRecords()
    parent = models.ForeignKey(Customer, related_name='pallet_set', verbose_name=_('customer'))
    is_closed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('pallet-purchase-list', kwargs={'customer_pk': self.parent.pk, 'pallet_pk': self.pk})

    def get_delete_url(self):
        return reverse('pallet-delete', kwargs={'customer_pk': self.parent.pk, 'pallet_pk': self.pk, })

    def get_export_url(self):
        return reverse('pallet-export', kwargs={'customer_pk': self.parent.pk, 'pallet_pk': self.pk, })

    class Meta(ChildMetaMixin):
        verbose_name = _('pallet')
        verbose_name_plural = _('pallets')



class PalletPurchase(AbstractTreeItem, HistoryURLMixin):
    history = HistoricalRecords()
    parent = models.ForeignKey(Pallet, verbose_name=_('pallet'))
    box = models.ForeignKey(Box, verbose_name=_('box'))
    product = models.ForeignKey(Product, )
    quantity_override = models.PositiveIntegerField(default=None, null=True, blank=True, verbose_name=_('quantity'))
    order_override = models.CharField(max_length=120, verbose_name=_('order'), blank=True, null=True, )

    def get_delete_url(self):
        return reverse('pallet-purchase-delete',
                       kwargs={'customer_pk': self.parent.parent.pk, 'pallet_pk': self.parent.pk,
                               'palletpurchase_pk': self.pk})

    def get_edit_url(self):
        return reverse('pallet-purchase-update',
                       kwargs={'customer_pk': self.parent.parent.pk, 'pallet_pk': self.parent.pk,
                               'palletpurchase_pk': self.pk})

    # @property
    # def name(self):
    #     return self.pallet.name
    #
    # @property
    # def barcode(self):
    #     return self.product.barcode

    # @property
    # def box(self):
    #     return self.box

    # @property
    # def order(self):
    #     return self.product.order if self.order_override is None else self.order_override
    #
    # @order.setter
    # def order(self, value):
    #     self.order_override = value
    #
    # @property
    # def quantity(self):
    #     return self.product.quantity if self.quantity_override is None else self.quantity_override
    #
    # @quantity.setter
    # def quantity(self, value):
    #     self.quantity_override = value

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = _('pallet purchase')
        verbose_name_plural = _('pallet purchases')
        unique_together = ('parent',)


PRIORITY = (Customer, Box, PalletPurchase, Pallet, )