# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-30 02:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personal', '0002_article_type_type_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article_type',
            old_name='user',
            new_name='user_id',
        ),
    ]
