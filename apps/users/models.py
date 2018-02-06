# encoding=utf-8
from __future__ import unicode_literals
from datetime import datetime
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    # 扩展系统User表
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(("male", '男'), ('female', '女')), default='male')
    address = models.CharField(max_length=100, default='')
    mobile = models.CharField(max_length=11, null=True, blank=True)

    image = models.ImageField(upload_to='image/%Y/%m', default='image/default.png', max_length=100)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.username


class EmailVerifyRecord(models.Model):
    # 邮箱验证码
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(choices=(('register', '注册'), ('forget', '找回密码')), max_length=10, verbose_name='验证码类型')
    # 邮箱验证码在注册和找回密码时都需要发送验证码
    send_time = models.DateTimeField(default=datetime.now, verbose_name='发送时间')

    # 方便设置过期时间

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)


class Banner(models.Model):
    # 轮播图
    title = models.CharField(max_length=100, verbose_name='标题')
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name='轮播图', max_length=100, default='image/default.png')
    # 实际储存的是图片的路径,Char类型
    url = models.URLField(max_length=200, verbose_name='访问地址')
    index = models.IntegerField(default=100, verbose_name='顺序')
    # 轮播图的顺序
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name
