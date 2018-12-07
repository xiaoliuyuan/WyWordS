from django.conf.urls import url

from . import views

urlpatterns = [
    # 主页
    url(r'^$', views.index),
    url(r'^index/$', views.index, name='index'),
    # 登录
    url(r'^login/$', views.user_login, name='login'),
    # 注册
    url(r'^register/$', views.register, name='register'),
    # 验证码
    url(r'^code/$', views.code, name='code'),
    # 邮箱
    # url(r'^email/$', views.send_email, name='email'),
    # 注销
    url(r'exit/$', views.exit, name='exit')
]
