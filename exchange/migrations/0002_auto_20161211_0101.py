# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-11 01:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange',
            name='category',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='exchange.Category'),
        ),
        migrations.AddField(
            model_name='exchange',
            name='link',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]