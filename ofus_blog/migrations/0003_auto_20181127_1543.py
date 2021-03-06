# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-27 07:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ofus_blog', '0002_users_email_verify'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=40, verbose_name='文章标题')),
                ('content', mdeditor.fields.MDTextField()),
                ('publishTime', models.DateTimeField(auto_now_add=True, verbose_name='创建文章的时间')),
                ('modifyTime', models.DateTimeField(auto_now=True, verbose_name='每次修改文章的时间')),
                ('Introduction', models.CharField(blank=True, max_length=255, null=True, verbose_name='文章简介')),
            ],
        ),
        migrations.AlterField(
            model_name='users',
            name='gender',
            field=models.CharField(default='未设置', max_length=10, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='users',
            name='header',
            field=models.ImageField(default='static/images/注册头像.png', upload_to='static/images/head', verbose_name='头像'),
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ofus_blog.Users'),
        ),
    ]
