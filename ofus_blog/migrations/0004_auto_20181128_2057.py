# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-28 12:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ofus_blog', '0003_auto_20181127_1543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.DeleteModel(
            name='Article',
        ),
    ]
