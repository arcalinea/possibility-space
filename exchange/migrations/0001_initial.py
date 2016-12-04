# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-04 03:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('request_date', models.DateTimeField(verbose_name='date requested')),
                ('deliver_date', models.DateTimeField(verbose_name='date delivered')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
                ('password', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=1000)),
                ('num_invited', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='exchange',
            name='giver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='giver', to='exchange.User'),
        ),
        migrations.AddField(
            model_name='exchange',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='exchange.User'),
        ),
    ]