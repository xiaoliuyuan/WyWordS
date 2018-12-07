from django.conf.urls import url

from . import views


urlpatterns = [

    # it分类
    url(r'^it/$', views.it, name='it'),
    # 绘画
    url(r'^draw/$', views.draw, name='draw'),
    # 想法
    url(r'^idea/$', views.draw, name='idea'),
    # 生活
    url(r'^live/$', views.draw, name='live'),
]