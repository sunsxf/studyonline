# encoding=utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from .models import UserProfile, EmailVerifyRecord, Banner
from django.db.models import Q
from django.views.generic import View
from .myforms import LoginForm, RegisterForm, ForgetForm, RestPwdForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_verify_email
from django.core.urlresolvers import reverse
import re, redis
from django.http import HttpResponse, HttpResponseRedirect
from courses.models import Course
from organization.models import CourseOrg


# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except:
            return None


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            # if user and user.is_active:
            if user:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html')
                else:
                    return render(request, 'login.html', {'err': '用户未激活'})
            else:
                return render(request, 'login.html', {'err': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'loginform': loginform})


class RegisterView(View):
    def get(self, request):
        registerform = RegisterForm()
        return render(request, 'register.html', {'registerform': registerform})

    def post(self, request):
        registerform = RegisterForm(request.POST)
        if registerform.is_valid():
            username = request.POST.get('email', '')
            email = username
            if UserProfile.objects.get(email=email):
                return render(request, 'register.html', {'msg': '邮箱已存在', 'registerform': registerform})
                # 传回registerform将用户信息回填
            password = request.POST.get('password', '')
            user = UserProfile()
            user.username = username
            user.email = email
            user.password = make_password(password)
            user.is_active = 0
            user.save()
            # 先将用户注册的信息入数据库,但未激活,is_active置为0
            send_verify_email(email, 'register')
            return render(request, 'login.html', {'registerform': registerform})
        else:
            return render(request, 'register.html', {'registerform': registerform})


class ForgetPwdView(View):
    def get(self, request):
        forgetpwdform = ForgetForm()
        return render(request, 'forgetpwd.html', {'forgetpwdform': forgetpwdform})

    def post(self, request):
        forgetpwdform = ForgetForm(request.POST)
        if forgetpwdform.is_valid():
            email = request.POST.get('email', '')
            send_verify_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {'forgetpwdform': forgetpwdform})


class ActiveView(View):
    def get(self, request, active_code):
        # 进入这个函数证明用户已经点击确认注册邮箱按钮,故将该用户变为激活状态
        # 当然前提是这个active_code是正确的
        record = EmailVerifyRecord.objects.get(code=active_code)
        if record:
            email = record.email
            user = UserProfile.objects.get(email=email)
            user.is_active = True
            user.save()
            # 修改数据后也要保存
            # filter方法返回列表;get返回唯一值,或报错
            # 此时用户才真正地注册成功
            return render(request, 'login.html')
        else:
            return render(request, 'active_fail.html')


class ResetPwdView(View):
    def get(self, request, reset_code):
        # 进入这个函数证明用户已经点击确认注册邮箱按钮,故将该用户变为激活状态
        # 当然前提是这个active_code是正确的
        record = EmailVerifyRecord.objects.get(code=reset_code)
        if record:
            email = record.email
            return render(request, 'password_reset.html', {'email': email})
            # 传入email好让后台处理逻辑时知道是哪个email(在收到的html页面又以hidden
            # 的input标签传回给post方法)
        else:
            return render(request, 'active_fail.html')


class ModifyPwdView(View):
    def post(self, request):
        resetpwdform = RestPwdForm(request.POST)
        if resetpwdform.is_valid():
            password = request.POST.get('password', '')
            password2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if password != password2:
                return render(request, 'password_reset.html', {'email': email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(password)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'resetpwdform': resetpwdform})


class IndexView(View):
    def get(self, request):
        all_banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {'all_banners': all_banners,
                                              'courses': courses,
                                              'banner_courses': banner_courses,
                                              'orgs': orgs})


def page_not_found(request):
    # 全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    # 全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
