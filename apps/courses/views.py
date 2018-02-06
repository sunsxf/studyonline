# coding=utf-8
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import Course, CourseResource
from operation.models import UserFavorite, CourseComment, UserCourse
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.


class CourseListView(View):
    def get(self, request):
        courses = Course.objects.order_by('-add_time')
        # 默认按最新排序
        hot_courses = Course.objects.order_by('-click_nums')[:3]

        # 全局搜索
        keywords = request.GET.get('keywords', '')
        if keywords:
            courses = courses.filter(Q(name__icontains=keywords) |
                                     Q(desc__icontains=keywords) |
                                     Q(detail__icontains=keywords))

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                courses = courses.order_by('-click_nums')
            elif sort == 'students':
                courses = courses.order_by('-students')
        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # p = Paginator(objects, request=request)
        p = Paginator(courses, 3, request=request)
        # 注意第二个参数为必填, 每页条数
        # people = p.page(page)
        page_courses = p.page(page)
        return render(request, 'course-list.html', {
            'courses': page_courses,
            'sort': sort,
            'hot_courses': hot_courses,
        })


class CourseDetailView(View, LoginRequiredMixin):
    '''课程详情页'''

    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        # test = Course.objects.filter(lesson__name__icontains='二')
        course.click_nums += 1
        course.save()
        # 当进入此视图时代表用户浏览(点击)了某课程详情,故课程点击数加1,保存!
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:2]
        else:
            relate_courses = []
        # 若没有tag, 传入模板时会报错
        # 由于模板中会遍历relate_courses,故其零值为空列表
        return render(request, 'course-detail.html', {'course': course,
                                                      'relate_courses': relate_courses,
                                                      'has_fav_org': has_fav_org,
                                                      'has_fav_course': has_fav_course, })


class CourseInfoView(LoginRequiredMixin, View):
    '''课程视频信息,推荐相关课程'''

    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.students += 1
        course.save()

        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
        # 判断用户是否已学习该课程,若没有,则保存到UserCourse表中

        user_courses = UserCourse.objects.filter(course=course)
        # 学过该课程的所有用户(UserCourse对象)
        user_ids = [course_user.user.id for course_user in user_courses]
        # 所有用户的id列表
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids).exclude(user=request.user)
        # 所有学过该课程的所有UserCourse对象(数组)
        # 除去该用户本身
        course_ids = [user_course.course.id for user_course in all_user_courses]
        # 所有学过该课程的所有用户的所有课程id
        # 多取一道课程ID是为了课程去重
        relate_courses = Course.objects.filter(id__in=course_ids).exclude(id=course_id).order_by('-click_nums')[:3]
        # 除去自身这门课程的id
        # 相关推荐课程
        return render(request, 'course-video.html', {'course': course,
                                                     'relate_courses': relate_courses})


class CourseCommentView(LoginRequiredMixin, View):
    '''课程评论'''

    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        resources = CourseResource.objects.filter(course=course).all()
        comments = CourseComment.objects.all().order_by('-add_time')
        return render(request, 'course-comment.html', {'course': course,
                                                       'resources': resources,
                                                       'comments': comments})


class AddCommentView(View):
    '''添加课程评论'''

    def post(self, request):
        if not request.user.is_authenticated():
            '''评论需验证用户登录'''
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')

        course_id = request.POST.get('course_id', 0)
        comment = request.POST.get('comment', '')
        if course_id and comment:
            # 评论和对应课程都不能为空
            course_comment = CourseComment()
            course = Course.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.user = request.user
            course_comment.comment = comment
            course_comment.save()
            return HttpResponse('{"status": "success", "msg": "发表成功"}', content_type='application/json')
        else:
            return HttpResponse('{"status": "fail", "msg": "发表失败"}', content_type='application/json')
