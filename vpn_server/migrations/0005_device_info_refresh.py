# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-08 07:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpn_server', '0004_remove_device_info_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='device_info',
            name='refresh',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
