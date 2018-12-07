from django.db import models
from django.contrib.auth.models import User
# MarkDown
from mdeditor.fields import MDTextField
# Create your models here.


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11, default='未设置', verbose_name='电话')
    age = models.IntegerField(default=1, verbose_name='用户年龄')
    gender = models.CharField(max_length=10, default='未设置', verbose_name='性别')
    header = models.ImageField(upload_to='static/images/head', default='static/images/注册头像.png', verbose_name='头像')
    email_verify = models.CharField(max_length=1, default=0, verbose_name='邮箱验证')
    user = models.OneToOneField(User, on_delete=models.CASCADE)


# class Article(models.Model):
#     id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=40, verbose_name='文章标题')
#     content = MDTextField()
#     publishTime = models.DateTimeField(auto_now_add=True, verbose_name='创建文章的时间')
#     modifyTime = models.DateTimeField(auto_now=True, verbose_name='每次修改文章的时间')
#     Introduction = models.CharField(max_length=255, null=True, blank=True, verbose_name='文章简介')
#
#     # 外键 on_delete=models.CASCADE级联删除
#     author = models.ForeignKey(Users, on_delete=models.CASCADE)

