# coding=utf-8
from django import forms
import re

from operation.models import UserAsk

class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self): # 固定写法
        '''可在此函数中自定义表单验证'''
        mobile = self.cleaned_data['mobile']
        pattern = '^1[3789]\d{9}'
        if re.match(pattern, mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码无效', code='mobile_invalid')
            # 固定写法

