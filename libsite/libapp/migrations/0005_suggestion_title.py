# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-14 23:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('libapp', '0004_auto_20160614_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion',
            name='title',
            field=models.CharField(default=datetime.datetime(2016, 6, 14, 23, 10, 20, 163116, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
    ]
