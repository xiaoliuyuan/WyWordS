import string
import random
from django.http import HttpResponse
# redis缓存
from django.core.cache import cache
# celery异步
from celery import Celery
# 邮箱
from django.core.mail import send_mail
# settings模块
from django.conf import settings


# 生成四位随机字符串
def getRandomChar(count=4):
    # 生成随机字符串
    # string模块包含各种字符串，以下为小写大写加数字
    ran = string.ascii_uppercase + string.ascii_lowercase + string.digits
    char = ''
    for i in range(count):
        char += random.choice(ran)
    return char


# 邮件
def send_email(em, username):
    # 四位随机数
    email = getRandomChar()

    # # 将邮箱验证码保存到session中
    # request.session['email'] = email

    # html样式
    msg = '<p target="_blank" style="font-weight:700px; font-size:30px;">'+email+'</p>'
    # 判断redis如果没有缓存就发送
    if not cache.get(username):
        # 发送
        # send_mail('OFUS激活验证码', '内容', settings.EMAIL_FROM, [em], html_message=msg)
        send_mail('OFUS激活验证码', '内容', settings.EMAIL_FROM, [em], html_message=msg)
        # 邮箱验证码保存到redis
        cache.set(username, email, 60 * 3)
    # print('redis缓存的', cache.get(username))

    return HttpResponse('ok')