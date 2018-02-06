# coding=utf-8
from django.conf.urls import url

from .views import OrgListView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavorView
from .views import TeacherListView, TeacherDetailView

urlpatterns = [
    url('^list/$', OrgListView.as_view(), name="org_list"),  # 课程机构列表页
    url('^add_ask/$', AddUserAskView.as_view(), name="add_ask"),
    url('^home/(?P<org_id>\d+?)/$', OrgHomeView.as_view(), name="org_home"),
    url('^course/(?P<org_id>\d+?)/$', OrgCourseView.as_view(), name="org_course"),
    url('^desc/(?P<org_id>\d+?)/$', OrgDescView.as_view(), name="org_desc"),
    url('^org_teacher/(?P<org_id>\d+?)/$', OrgTeacherView.as_view(), name="org_teacher"),

    url('^add_fav/$', AddFavorView.as_view(), name="add_fav"),
    # 收藏课程机构
    url('^teacher/list/$', TeacherListView.as_view(), name="teacher_list"),
    # 讲师详情页
    url('^teacher/detail/(?P<teacher_id>\d+?)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]