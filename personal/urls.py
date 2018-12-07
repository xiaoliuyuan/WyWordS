from django.conf.urls import url

from . import views

urlpatterns =[
    # 个人主页
    url(r'^one_people/$', views.one_people, name='one_people'),
    # 邮箱验证
    url(r'^email_verify/$', views.email_verify, name='email_verify'),
    # 个人资料
    url(r'^one_date/$', views.one_date, name='one_date'),
    # 个人头像
    url(r'^one_date_head/$', views.one_date_head, name='one_date_head'),
    # 发表文章
    url(r'^send_article/$', views.send_article, name='send_article'),
    # 管理文章
    url(r'^manage_article/$', views.manage_article, name='manage_article'),
    # 创建分类
    url(r'^create_type/$', views.create_type, name='create_type'),
    # 文章分类
    url(r'article_inquire/$', views.article_inquire, name='article_inquire')
]