# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20150904_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='in_close',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customer',
            name='time_close',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 26, 23, 25, 34, 205639)),
        ),
        migrations.AddField(
            model_name='historicalcustomer',
            name='in_close',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalcustomer',
            name='time_close',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 26, 23, 25, 34, 205639)),
        ),
    ]
