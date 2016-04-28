from django.conf.urls import url

from .views import (
    CustomerListView,
    BoxListView,
    ProductListView,

    CustomerCreateView,
    BoxCreateView,
    ProductCreateView,

    CustomerDeleteView,
    BoxDeleteView,
    ProductDeleteView,
    BoxExportView,
    BoxToggleCloseView,
    CustomerExportView,
    CustomerUpdateView,

    ProductSearchView,
    ProductUpdateView,

    LogsView,
    LogsExportView,

    CustomerArchiveView,

    PalletListView,
    PalletCreateView,
    PalletDeleteView,
    PalletExportView,
    PalletToggleCloseView,
    PalletPurchaseListView,
    PalletPurchaseCreateView,

    BoxPalletListView
)

from .views import rename_box, import_file_page

urlpatterns = (

    url(r'^logs/$', LogsView.as_view(), name='logs'),

    url(r'^logs/export/$', LogsExportView.as_view(), name='logs_export'),

    url(r'^customers/$', CustomerListView.as_view(), name='customer-list'),

    url(r'^boxes/(?P<pk>\d+)/toggle-close/$', BoxToggleCloseView.as_view(), name='box-toggle-close'),

    url(r'^products/(?P<barcode>\d+)/$', ProductSearchView.as_view(), name='product-search'),

    url(r'^customers/(?P<pk>\d+)/edit/$', CustomerUpdateView.as_view(), name='customer-update'),

    url(r'^customers/create/$', CustomerCreateView.as_view(), name='customer-create'),

    url(r'^customers/archive/$', CustomerArchiveView.as_view(), name='customer-archive'),

    url(r'^customers/(?P<customer_pk>\d+)/delete/$', CustomerDeleteView.as_view(), name='customer-delete', ),

    url(r'^customers/(?P<customer_pk>\d+)/export/$', CustomerExportView.as_view(), name='customer-export', ),

    url(r'^customers/(?P<customer_pk>\d+)/boxes/$', BoxListView.as_view(), name='box-list'),

    url(r'^customers/(?P<customer_pk>\d+)/boxes/create/$', BoxCreateView.as_view(), name='box-create'),

    url(r'^customers/(?P<customer_pk>\d+)/boxes/(?P<box_pk>\d+)/delete/$', BoxDeleteView.as_view(), name='box-delete'),

    url(r'^customers/(?P<customer_pk>\d+)/boxes/(?P<box_pk>\d+)/export/$', BoxExportView.as_view(), name='box-export'),

    url(r'^customers/(?P<customer_pk>\d+)/boxes/(?P<box_pk>\d+)/products/$', ProductListView.as_view(),
        name='product-list'),

    url(r'^customers/(?P<customer_pk>\d+)/boxes/(?P<box_pk>\d+)/products/(?P<productpurchase_pk>\d+)/delete/$',
        ProductDeleteView.as_view(), name='product-delete'),

    url(r'^customers/(?P<customer_pk>\d+)/boxes/(?P<box_pk>\d+)/products/(?P<productpurchase_pk>\d+)/update/$',
        ProductUpdateView.as_view(), name='product-update'),

    url(r'^customers/(?P<customer_pk>\d+)/boxes/(?P<box_pk>\d+)/products/rename_box/$', rename_box),

    url(r'^customers/(?P<customer_pk>\d+)/pallets/(?P<pallet_pk>\d+)/pallet_purchase/rename_box/$', rename_box),

    url(r'^customers/(?P<customer_pk>\d+)/boxes/(?P<box_pk>\d+)/products/import_file_page/$', import_file_page),

    url(r'^customers/(?P<customer_pk>\d+)/boxes/(?P<box_pk>\d+)/products/create/$', ProductCreateView.as_view(),
        name='product-create'),


    url(r'^customers/(?P<customer_pk>\d+)/$', BoxPalletListView.as_view(), name='box-pallet'),


    url(r'^customers/(?P<customer_pk>\d+)/pallets/$', PalletListView.as_view(), name='pallet-list'),

    url(r'^customers/(?P<customer_pk>\d+)/pallets/create/$', PalletCreateView.as_view(), name='pallet-create'),

    url(r'^customers/(?P<customer_pk>\d+)/pallets/(?P<pallet_pk>\d+)/delete/$', PalletDeleteView.as_view(),
        name='pallet-delete'),

    url(r'^customers/(?P<customer_pk>\d+)/pallets/(?P<pallet>\d+)/export/$', PalletExportView.as_view(),
        name='pallet-export'),

    url(r'^customers/(?P<customer_pk>\d+)/pallets/(?P<pallet_pk>\d+)/pallet_purchase/$',
        PalletPurchaseListView.as_view(), name='pallet-purchase-list'),

    url(r'^customers/(?P<customer_pk>\d+)/pallets/(?P<pallet_pk>\d+)/pallet_purchase/create/$',
        PalletPurchaseCreateView.as_view(), name='pallet-purchase-create'),

    url(r'^customers/(?P<customer_pk>\d+)/pallets/(?P<pallet_pk>\d+)/pallet_purchase/import_file_page/$',
        import_file_page),)
