from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse

from django.contrib.auth import models
from ofus_blog.models import Users
"""
    所有分类共享一个页面，查询的数据不同
"""


# cookie 装饰器
def auth(func):
    def inner(request, *args, **kwargs):
        v = request.COOKIES.get('user_cookie')
        if not v:
            return redirect(reverse('ofus_blog:index'))
        return func(request, *args, **kwargs)
    return inner


# 获取cookie
def cookie(request):
    v = request.COOKIES.get('user_cookie')
    return v


# 判断邮箱是否验证
def email_auth(func):
    def inner(request, *args, **kwargs):
        cook = request.COOKIES.get('user_cookie')
        # 如果不存在cook
        if cook:
            user = models.User.objects.get(username=cook)
            users = Users.objects.get(user_id=user.id)
            if users.email_verify == '0':
                # 跳转到邮箱验证页面
                return redirect(reverse('personal:email_verify'))
        return func(request, *args, **kwargs)
    return inner


# it
@email_auth
def it(request):
    cook = cookie(request)
    # 内置用户表
    return render(request, 'sort/sort.html', {'msg': cook})


# draw画
@email_auth
def draw(request):
    cook = cookie(request)
    return render(request, 'sort/sort.html', {'msg': cook})


# idea想法
@email_auth
def idea(request):
    cook = cookie(request)
    return render(request, 'sort/sort.html', {'msg': cook})


# live生活
@email_auth
def live(request):
    cook = cookie(request)
    return render(request, 'sort/sort.html', {'msg': cook})
