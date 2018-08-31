# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-08-09 21:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='updated_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
