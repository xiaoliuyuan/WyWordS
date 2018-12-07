from django.shortcuts import render
from django.shortcuts import redirect, reverse
# model,QuerySet 序列化成json
from django.core import serializers

from django.http import JsonResponse
# 引入内置models
from django.contrib.auth.models import User
# 引入用户信息
from ofus_blog.models import Users
# 引入工具包
from . import utils
# redis缓存
from django.core.cache import cache
# 用户验证登录方法
from django.contrib.auth.decorators import login_required
# 获取时间
from django.utils import timezone

# MarkDown
import markdown

from . import models

import re


# 获取cookie
def cookie(request):
    v = request.COOKIES.get('user_cookie')
    return v


# 装饰器判断邮箱是否验证
def email_auth(func):
    def inner(request, *args, **kwargs):
        # 获取cookie
        try:
            cook = request.COOKIES.get('user_cookie')
            # 如果不存在cookie
            if cook:
                user = User.objects.get(username=cook)
                users = models.Users.objects.get(user_id=user.id)
                if users.email_verify == '0':
                    # 跳转到邮箱验证页面
                    return redirect(reverse('personal:email_verify'))
        except:
            return redirect(reverse('ofus_blog:login'+'?xuyaologin'))
        return func(request, *args, **kwargs)
    return inner


# 个人主页
@email_auth
def one_people(request):
    cookie_user = cookie(request)
    print('123456432134567543', request.user.id)
    return render(request, 'personal/one_people.html', {'msg': cookie_user})


# 个人资料
@login_required
def one_date(request):
    if request.method == 'GET':
        return render(request, 'personal/one_date.html')

    elif request.method == 'POST':  # 到底用那种方法 get传还是 session - request.user传
        gender = request.POST['gender']
        email = request.POST['email']
        print(gender, email)
        try:
            user = models.User.objects.get(username=request.user.username)
            print(user.email)
            user.email = email
            users = Users.objects.get(user_id=user.id)
            print(users.gender)
            users.gender = gender
            user.save()
            users.save()
            return redirect(reverse('personal:one_date'))
        except:
            return render(request, 'personal/one_date.html', {'msg': '错误'})


# 个人头像
def one_date_head(request):
    # 获得Users用户信息
    users = Users.objects.get(user_id=request.user.id)
    if request.method == 'GET':
        return render(request, 'personal/one_date_head.html', {'users': users})
    elif request.method == 'POST':
        # 修改头像
        head = request.FILES['head']
        print(head)
        img = r'^.*(jpg|png)$'
        if re.search(img, str(head)):
            users.header = head
            users.save()
            return render(request, 'personal/one_date_head.html', {'users': users})

    return render(request, 'personal/one_date_head.html', {'msg': '文件错误'})


# 发表文章页面
def send_article(request):
    # GET请求
    if request.method == 'GET':
        # 如果查询到数据
        try:
            article_type = models.article_type.objects.filter(user_id=request.user.id)
            # print(article_type.type_title)
            if article_type:
                # 默认显示已经存在的
                return render(request, 'personal/send_article.html', {'article_type': article_type})
            else:
                raise Exception("用户点击的分类没有文章数据")
        # 如果查询不到数据
        except:
            return render(request, 'personal/send_article.html')
    # POST请求
    elif request.method == 'POST':
        # 获得文本
        title = request.POST['title']
        content = request.POST['my-editormd-html-code']

        return render(request, 'personal/send_article.html')


# 创建文章分类的时候默认创建一篇文章
def create_type(request):
    # 获取用户输入的类型名称
    create_type = request.POST['create_type']
    # 创建文章分类
    create = models.article_type(user_id=request.user.id, type_title=create_type)
    # 保存
    create.save()
    # 获取当前日期
    date = timezone.now().strftime('%Y-%m-%d')
    # 创建一篇空的默认文章
    create_article = models.article(title=date, article_type_id=create.id)
    # 保存
    create_article.save()
    # 返回Json数据
    return JsonResponse(create_type, safe=False)


# 分类文章查询
def article_inquire(request):
    # 前台传来的文章分类
    inquire_type = request.POST['type']
    type = models.article_type.objects.get(type_title=inquire_type)
    # 把QuerySet转成json
    # ajax_articles = serializers.serialize('json', models.article.objects.filter(article_type=type.id))
    articles = models.article.objects.filter(article_type=type.id)
    # 文章名称存入列表
    articles_list = []
    for a in articles:
        articles_list.append(a.title)
    return JsonResponse(articles_list, safe=False)


# 管理文章
def manage_article(request):
    pass


# 验证邮箱
def email_verify(request):
    # 获取cookie用户名
    cookie_user = cookie(request)
    if request.method == 'GET':
        try:
            # 根据用户名查询用户
            user = User.objects.get(username=cookie_user)
            print('1111111', user)
            # 查询用户额外信息
            # users = Users.objects.get(user_id=user.id)
            print('1111111', user)
            # 发送邮件
            print(user.email, user.username)
            utils.send_email(user.email, user.username)
            return render(request, 'personal/email_verify.html', {'email': user.email, 'msg': cookie_user})
        except Exception as e:
            print(e)
            return render(request, 'personal/email_verify.html')

    elif request.method == 'POST':
        # 获取邮箱验证码
        code = request.POST['code']
        # 获取redis
        email_code = cache.get(cookie_user)
        # 验证
        if code == email_code:
            # 根据用户名查询用户
            user = User.objects.get(username=cookie_user)
            users = Users.objects.get(user_id=user.id)
            # 设置为 1 （绑定邮箱模式）
            users.email_verify = '1'
            users.save()
            return redirect(reverse('ofus_blog:index'))
        else:
            # 根据用户名查询用户
            user = models.User.objects.get(username=cookie_user)
            return render(request, 'personal/email_verify.html', {'email': user.email, 'warning': '验证码填写错误,已重新发送验证码', 'msg':cookie_user})




