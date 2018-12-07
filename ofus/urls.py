"""ofus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # 主页
    url(r'^', include('ofus_blog.urls', namespace='ofus_blog')),
    # 分类
    url(r'^sort/', include('sort.urls', namespace='sort')),
    # 个人主页
    url(r'^personal/', include('personal.urls', namespace='personal')),
    # MarkDown
    url(r'^mdeditor/', include('mdeditor.urls'))

]
