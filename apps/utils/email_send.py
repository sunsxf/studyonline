# encoding=utf-8
__author__ = 'sxf'
from random import Random
from django.core.mail import send_mail
from users.models import EmailVerifyRecord
from studyonline.settings import EMAIL_FROM


def gen_random_str(randomlength=8):
    str_ = ''
    chars_ = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    length = len(chars_) - 1
    random_ = Random()
    for i in range(randomlength):
        str_ += chars_[random_.randint(0, length)]
    return str_


def send_verify_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    code = gen_random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()
    # 将需要发送给用户的随机字符串(code)先保存在数据库中
    if send_type == 'register':
        subject = '元智在线网激活链接'
        message = '请点击以下链接激活你的帐号:http://127.0.0.1:8000/active/{0}'.format(code)
        send_status = send_mail(subject, message, EMAIL_FROM, [email])
        # 返回布尔值
        if send_status:
            pass
    if send_type == 'forget':
        subject = '元智在线网密码重置链接'
        message = '请点击以下链接重置密码:http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(subject, message, EMAIL_FROM, [email])
        # 返回布尔值
        if send_status:
            pass
