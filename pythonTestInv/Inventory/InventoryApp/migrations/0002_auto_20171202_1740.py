# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 17:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('InventoryApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inv_location',
            name='statusId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InventoryApp.inv_status'),
        ),
    ]
