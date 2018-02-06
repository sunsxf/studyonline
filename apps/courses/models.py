# encoding=utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from organization.models import CourseOrg, Teacher


# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name='课程名')
    course_org = models.ForeignKey(CourseOrg, verbose_name='课程机构', null=True, blank=True)
    desc = models.CharField(max_length=200, verbose_name='课程描述')
    detail = models.TextField(verbose_name='课程详情')
    degree = models.CharField(max_length=2, choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), verbose_name='难度')
    is_banner = models.BooleanField(default=False, verbose_name='是否轮播')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    image = models.ImageField(max_length=100, upload_to='courses/%Y/%m', verbose_name='封面图',
                              default='image/default.png')
    category = models.CharField(max_length=50, verbose_name='课程类别', default='后端开发')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    tag = models.CharField(max_length=50, verbose_name='课程标签', default='')
    teacher = models.ForeignKey(Teacher, verbose_name='课程讲师', null=True, blank=True)
    need_to_know = models.CharField(max_length=200, verbose_name='课程须知', default='')
    tell_you_what = models.CharField(max_length=200, verbose_name='老师告诉你', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_lesson_nums(self):
        # 获取某课程章节数
        return self.lesson_set.all().count()

    get_lesson_nums.short_description = '章节数'

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe('<a href="http://www.baidu.com">test跳转</a>')

    go_to.short_description = '跳转链接'

    def get_learn_users(self):
        # 获取学习某课程人数,self.usercourse_set调用all()方法后才是QuerySet对象
        return self.usercourse_set.all()[:5]

    def get_lessons(self):
        # 获取课程所有章节
        return self.lesson_set.all()

    def get_resourses(self):
        # 获取课程所有下载资源
        return self.courseresource_set.all()


class BannerCourse(Course):
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True  # 不写就会再生成一张表


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程名')
    name = models.CharField(max_length=100, verbose_name='章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '({0}){1}'.format(self.course, self.name)

    def get_videos(self):
        '''获取课程所有的视频'''
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name='章节')
    name = models.CharField(max_length=100, verbose_name='视频名')
    url = models.CharField(max_length=100, verbose_name='视频地址', default='')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='资源名称')
    download = models.FileField(max_length=100, upload_to='course/resource/%Y/%m', verbose_name='课程资源文件')
    # 文件类型,如果定义文件类型的字段,在后台管理系统中会自动生成上传按钮
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name
