from django.db import models
from ofus_blog.models import Users
# Create your models here.

# MarkDown
from mdeditor.fields import MDTextField


# 文章分类
class article_type(models.Model):
    # 编号
    id = models.AutoField(primary_key=True)
    # 分类名称
    type_title = models.CharField(max_length=20, default='默认文集', verbose_name='分类名称')
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 所属用户id外键
    user_id = models.CharField(max_length=255)


# 文章
class article(models.Model):
    # 编号
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=40, verbose_name='文章标题')
    content = MDTextField(default='')
    publishTime = models.DateTimeField(auto_now_add=True, verbose_name='创建文章的时间')
    modifyTime = models.DateTimeField(auto_now=True, verbose_name='每次修改文章的时间')
    Introduction = models.CharField(max_length=255, null=True, blank=True, verbose_name='文章简介')
    # 外键 关联分类
    article_type = models.ForeignKey(article_type, on_delete=models.CASCADE, verbose_name='分类')
