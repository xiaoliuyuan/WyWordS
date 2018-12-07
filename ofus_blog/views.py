# coding=utf-8
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, JsonResponse

# django内置认证模块
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

# 引入django的User表
from django.contrib.auth.models import User

# 引入models
from . import models
# 引入公共工具模块
from . import utils

# 引入IO模块
from io import BytesIO


# 主页
def index(request):
    cook = request.COOKIES.get('user_cookie')
    print(cook)
    return render(request, 'ofus_blog/index.html', {'msg': cook})


# 登录
def user_login(request):
    if request.method == 'GET':
        return render(request, 'ofus_blog/login.html')

    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        code = request.POST['code'].lower()
        print(username, password)

        # 验证码验证
        scode = request.session['code'].lower()
        if code != scode:
            del request.session['code']
            return render(request, 'ofus_blog/login.html', {'msg': '验证码错误'})

        # 验证登录
        user = authenticate(username=username, password=password)
        if user:
            # 验证过了就删除验证码
            del request.session['code']
            # login使用django的session框架给某个已认证的用户附加上session_id信息
            login(request, user)
            # request.session.set_expiry(0)
            response = redirect(reverse('ofus_blog:index'))
            # 添加cookie
            response.set_cookie('user_cookie', username, max_age=60 * 24 * 7)
            return response
        else:
            return render(request, 'ofus_blog/login.html', {'msg': '登录失败'})


# 注册
def register(request):
    if request.method == 'GET':
        return render(request, 'ofus_blog/register.html')
    elif request.method == 'POST':
        # 账号去除空格
        # username = ''.join(request.POST['username'].split())
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()
        email = request.POST['email'].strip()

        try:
            # 用户名验证 如果不存在就会报错
            User.objects.get(username=username)
            return render(request, 'ofus_blog/register.html', {'msg': '用户名已存在，请重新注册'})
        except:
            try:
                # create_user辅助函数创建用户
                user = User.objects.create_user(username=username, password=password)
                # 存邮箱
                user.email = email
                # 关联用户信息表
                usera = models.Users(user=user)
                user.save()
                usera.save()
                return render(request, 'ofus_blog/register.html', {'msg': '注册成功！'})
            except:
                return render(request, 'ofus_blog/register.html', {'msg': '内部错误,请重新注册'})


# 验证码
def code(request):
    img, code = utils.create_code()
    # 将code保存到session中
    request.session['code'] = code
    # print('验证码', code)
    # 返回图片
    # print(img)
    file = BytesIO()
    img.save(file, 'png')
    # print(file.getvalue())
    return HttpResponse(file.getvalue(), 'image/png')


# 注销
def exit(request):
    logout(request)

    response = redirect(reverse('ofus_blog:index'))
    response.delete_cookie('user_cookie')
    return response


# 判断邮箱是否验证
# def email_auth():
#     def inner(request, *args, **kwargs):
#         cook = request.COOKIES.get('user_cookie')
#         v = models.User.object.git(username=cook)
#         print(v)


