# encoding=utf-8
from __future__ import unicode_literals

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'  # 注意前面不要加apps,apps已被标记为sourceroot
    verbose_name = '用户信息'
