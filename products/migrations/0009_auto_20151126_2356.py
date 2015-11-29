# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_auto_20151126_2325'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='in_close_time',
            field=models.IntegerField(default=30),
        ),
        migrations.AddField(
            model_name='historicalcustomer',
            name='in_close_time',
            field=models.IntegerField(default=30),
        ),
        migrations.AlterField(
            model_name='customer',
            name='time_close',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 26, 23, 56, 56, 616030)),
        ),
        migrations.AlterField(
            model_name='historicalcustomer',
            name='time_close',
            field=models.DateTimeField(default=datetime.datetime(2015, 11, 26, 23, 56, 56, 616030)),
        ),
    ]
