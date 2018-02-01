# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-01 16:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('InventoryApp', '0011_auto_20180131_1455'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_menus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menuName', models.CharField(max_length=30)),
                ('jobRole', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InventoryApp.emp_jobrole')),
            ],
            options={
                'db_table': 'user_menus',
            },
        ),
    ]
