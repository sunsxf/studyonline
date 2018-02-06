# encoding=utf-8
__author__ = 'sxf'

import xadmin
from .models import City, CourseOrg, Teacher


class CityAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'add_time', 'city']
    search_fields = ['name', 'desc', 'click_nums', 'city__name']
    list_filter = ['name', 'desc', 'click_nums', 'add_time', 'city']
    relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'click_nums', 'add_time']
    search_fields = ['org__name', 'name', 'work_years', 'click_nums']
    list_filter = ['org', 'name', 'work_years', 'click_nums', 'add_time']


xadmin.site.register(City, CityAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
