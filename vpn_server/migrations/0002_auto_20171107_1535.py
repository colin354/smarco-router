# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-11-07 07:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vpn_server', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device_info',
            name='vpn_status',
            field=models.IntegerField(),
        ),
    ]
