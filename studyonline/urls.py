# encoding=utf-8
"""studyonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, ActiveView, ForgetPwdView, ResetPwdView, ModifyPwdView, LogoutView, IndexView
from organization.views import OrgListView
# from django.contrib import admin
import xadmin
from django.views.static import serve
from studyonline.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', IndexView.as_view(), name="index"),
    url('^login/$', LoginView.as_view(), name="login"),
    url('^logout/$', LogoutView.as_view(), name="logout"),
    url('^register/$', RegisterView.as_view(), name="register"),
    url('^captcha/', include('captcha.urls')),
    url('^active/(?P<active_code>.*)/$', ActiveView.as_view(), name="active"),
    # url('^flash/(?P<query_str>.*)/$', Flash.as_view(), name="flash"),
    url('^forgetpwd/$', ForgetPwdView.as_view(), name="forgetpwd"),
    url('^resetpwd/(?P<reset_code>.*)/$', ResetPwdView.as_view(), name="resetpwd"),
    url('^modifypwd/$', ModifyPwdView.as_view(), name="modifypwd"),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # 配置上传文件的访问处理函数
    # url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

    url('^org/', include('organization.urls', namespace='org')),
    url('^course/', include('courses.urls', namespace='course')),
    # url('^users/', include('users.urls', namespace='users')),
]

# 全局404配置
handler404 = 'users.views.page_not_found'

handler500 = 'users.views.page_error'