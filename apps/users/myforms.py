# encoding=utf-8
__author__ = 'sxf'

from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={'invalid': '验证码有误'})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码有误'})


class RestPwdForm(forms.Form):
    password = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)