# coding=utf-8
from django.conf.urls import url

from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView

urlpatterns = [
    url('^list/$', CourseListView.as_view(), name="course_list"),  # 课程列表页
    url('^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="course_detail"),
    # 课程详情页,哪个页面的详情?故需要一个course_id
    url('^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name="course_info"),
    url('^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name="course_comment"),
    url('^addcomment/$', AddCommentView.as_view(), name="course_addcomment"),
    # 添加课程评论
]
