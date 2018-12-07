import string
import random
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter
from django.http import HttpResponse

# 邮箱
from django.core.mail import send_mail
# settings模块
from django.conf import settings


# 生成四位随机字符串
def getRandomChar(count=4):
    # 生成随机字符串
    # string模块包含各种字符串，以下为小写大写加数字
    ran = string.ascii_uppercase + string.ascii_lowercase + string.digits
    print(ran)
    char = ''
    for i in range(count):
        char += random.choice(ran)
    return char


# 返回一个随机的RGB颜色
def getRandomColor():
    return (random.randint(50,150), random.randint(50,150), random.randint(50,150))


# 创建图片
def create_code():
    # 创建图片，模式，大小，背景色
    img = Image.new('RGB', (120, 20), (255, 255, 255))
    # 创建画布
    draw = ImageDraw.Draw(img)
    # 设置字体
    font = ImageFont.truetype('Deng.ttf', 18)

    # 随机字符
    code = getRandomChar()

    # 随机颜色
    # color = getRandomColor()

    # 将生成的字符画在画布上
    for t in range(4):
        draw.text((30*t+5, 0), code[t], getRandomColor(), font)

    # 生成干扰点
    # for _ in range(random.randint(0, 200)):
    #     # 位置，颜色
    #     draw.point((random.randint(0, 120), random.randint(0, 30)), fill=getRandomColor())

    # 使用模糊滤镜使图片模糊
    # images = images.filter(ImageFilter.BLUR)
    # 保存
    return img, code


# 邮件
def send_email(request, email):
    # 四位随机数
    email = getRandomChar()
    # 将邮箱验证码保存到session中
    request.session['email'] = email
    msg = '<p target="_blank" style="font-weight:700px; font-size:30px;">'+email+'</p>'
    send_mail('[OFUS激活验证码]', '内容', settings.EMAIL_FROM, ['949621184@qq.com'], html_message=msg)
    return HttpResponse('ok')