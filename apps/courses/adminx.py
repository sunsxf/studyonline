# encoding=utf-8
__author__ = 'sxf'

from .models import Course, Lesson, Video, CourseResource, BannerCourse
import xadmin


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'course_org', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'teacher',
                    'click_nums', 'get_lesson_nums', 'go_to', 'add_time']
    search_fields = ['name', 'course_org__name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums',
                     'teacher', 'click_nums']
    list_filter = ['name', 'course_org', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'teacher',
                   'click_nums', 'add_time']
    ordering = ['-click_nums']
    readonly_fields = ['click_nums']
    list_editable = ['degree', 'desc']
    exclude = ['fav_nums']
    inlines = [LessonInline, CourseResourceInline]
    refresh_times = [3, 5]

    def queryset(self):
        qs = super(CourseAdmin, self).queryset() # 得到queryset对象
        return qs.filter(is_banner=False)


class BannerCourseAdmin(object):
    list_display = ['name', 'course_org', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'teacher',
                    'click_nums',
                    'add_time']
    search_fields = ['name', 'course_org__name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums',
                     'teacher', 'click_nums']
    list_filter = ['name', 'course_org', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'teacher',
                   'click_nums', 'add_time']
    ordering = ['-click_nums']
    readonly_fields = ['click_nums']
    exclude = ['fav_nums']
    inlines = [LessonInline, CourseResourceInline]

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset() # 得到queryset对象
        return qs.filter(is_banner=True)


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course__name', 'name']
    list_filter = ['course', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'url', 'learn_times', 'add_time']
    search_fields = ['lesson__name', 'name', 'url', 'learn_times']
    list_filter = ['lesson', 'name', 'url', 'learn_times', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course__name', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
