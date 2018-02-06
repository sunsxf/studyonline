# encoding=utf-8
from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import CourseOrg, City, Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite


# Create your views here.

class OrgListView(View):
    def get(self, request):
        orgs = CourseOrg.objects.all()
        cities = City.objects.all()
        hot_orgs = orgs.order_by('-click_nums')[:3]

        # 全局搜索
        keywords = request.GET.get('keywords', '')
        if keywords:
            # orgs = CourseOrg.objects.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords))
            orgs = orgs.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))

        # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            # orgs = CourseOrg.objects.filter(city_id=int(city_id))
            orgs = orgs.filter(city_id=int(city_id))
            # 注意此时的查询对象是已经经过一次筛选的QuerySet
            # 保持orgs变量名不变,表示对orgs的进一步筛选
            # CourseOrg表有个外键字段(city)关联City表,在CourseOrg表内其实保存的是city_id字段(所有外键都是)

        # 对培训机构进行筛选
        category = request.GET.get('ct', '')
        if category:
            orgs = orgs.filter(category=category)
        # if city_id and category:
        #     orgs = CourseOrg.objects.filter(city_id=int(city_id), category=category)
        # elif city_id:
        #     orgs = CourseOrg.objects.filter(city_id=int(city_id))
        # elif category:
        #     orgs = CourseOrg.objects.filter(category=category)
        # 直接查库逻辑

        # 对学习人数和课程数进行倒序排序
        # 注意此类排序是在城市和机构筛选后再排序的,故逻辑上必须放在上面两层筛选后面,且筛选对象是已筛选处理后的QuerySet
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                orgs = orgs.order_by("-students")
            elif sort == 'course_nums':
                orgs = orgs.order_by("-course_nums")

        org_nums = orgs.count()  # 对课程数量的统计放在所有筛选动作之后

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        # p = Paginator(objects, request=request)
        p = Paginator(orgs, 5, request=request)
        # 注意第二个参数为必填, 每页条数
        # people = p.page(page)
        page_orgs = p.page(page)

        return render(request, 'org_list.html', {
            # 'orgs': orgs,
            'orgs': page_orgs,  # 这样就不会把所有的对象传递到模板,而是分页后传递
            'cities': cities,  # 模板里的page_obj对应此处的page_orgs,也即传入模板的orgs
            'org_nums': org_nums,  # 对传入模板的模型要调用object_list属性才能遍历(所有要分页的地方都要加此属性)
            'city_id': city_id,  # 将city_id传入,与用户点击时传递进来的city.id进行比对,若相等则给一个选中标识
            'category': category,  # 指明用户选定的是哪种category
            'hot_orgs': hot_orgs,
            'sort': sort,  # 当模板用到sort变量时,orgs是经过相应排序的
        })


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            userask = userask_form.save(commit=True)
            return HttpResponse('{"status": "success"}', content_type="application/json")
        else:
            return HttpResponse('{"status": "fail", "msg": "咨询失败"}', content_type="application/json")


class OrgHomeView(View):
    '''机构首页'''

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 通过前端页面访问时的url参数查库获得课程机构
        course_org.click_nums += 1
        course_org.save()
        all_courses = course_org.course_set.all()[:4]
        # course_org是一个CourseOrg模型的实例,Course表通过外键与其关联.此时course_org有个自动生成的变量(属性?)
        # course_set来反向取这个course_org的所有course
        teachers = course_org.teacher_set.all()
        current_page = 'home'
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_fav = True
        # 传入模板做收藏按钮标志位,如用户已登录且在收藏表中能查到相应记录,则将标志位置为True
        return render(request, 'org-detail-homepage.html', {'all_courses': all_courses,
                                                            'teachers': teachers,
                                                            'course_org': course_org,
                                                            'current_page': current_page,
                                                            'has_fav': has_fav,
                                                            })


class OrgCourseView(View):
    '''机构课程列表页'''

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        current_page = 'course'
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html', {'all_courses': all_courses,
                                                          'course_org': course_org,
                                                          'current_page': current_page,
                                                          'has_fav': has_fav,
                                                          })


class OrgDescView(View):
    '''机构介绍页'''

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        current_page = 'desc'
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {'course_org': course_org,
                                                        'current_page': current_page,
                                                        'has_fav': has_fav,
                                                        })


class OrgTeacherView(View):
    '''机构教师介绍页'''

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        teachers = course_org.teacher_set.all()
        current_page = 'teacher'
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=org_id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {'course_org': course_org,
                                                            'teachers': teachers,
                                                            'current_page': current_page,
                                                            'has_fav': has_fav,
                                                            })


class AddFavorView(View):
    '''用户收藏,取消收藏'''

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated():
            # 用户未登录,则无法进行收藏与取消收藏操作,此时request中依然有user变量,只不过是未登录的系统自带user变量
            return HttpResponse('{"status": "fail", "msg": "用户未登录"}', content_type='application/json')
        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        # 如果用户已登录,则结合用户,数据id,收藏类型三者联合查询用户收藏表中是否存在满足条件的数据
        if exist_record:
            # 如果存在,则表示该用户想要取消收藏,将UserFavor表中相应数据删除;不存在,则代表收藏操作
            exist_record.delete()
            if fav_type == '1':
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                course.save()
            elif fav_type == '2':
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                course_org.save()
            elif fav_type == '3':
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
            # 收藏数-1
                teacher.save()
            return HttpResponse('{"status": "success", "msg": "收藏"}', content_type='application/json')
        else:
            # 未查询到记录也可能是fav_id或fav_type为零
            if int(fav_id) and int(fav_type):
                user_fav = UserFavorite()
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                # 从表单获取的fav_id及fav_type都为字符串类型,而数据库中相应字段数据类型为整形,故需做类型转换
                user_fav.save()
                # 保存操作先实例化一个数据对象,然后对其字段进行赋值
                if fav_type == '1':
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif fav_type == '2':
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                elif fav_type == '3':
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                # 收藏数+1
                    teacher.save()
                return HttpResponse('{"status": "success", "msg": "已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status": "fail", "msg": "收藏失败"}', content_type='application/json')


class TeacherListView(View):
    '''教师列表页'''

    def get(self, request):
        teachers = Teacher.objects.all()

        rank_teachers = teachers.order_by('-click_nums')[:3]
        # 人气讲师排行

        # 全局搜索
        keywords = request.GET.get('keywords', '')
        if keywords:
            teachers = teachers.filter(name__icontains=keywords)

        sort = request.GET.get('sort', '')
        if sort == 'hot':
            teachers = teachers.order_by('-click_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(teachers, 5, request=request)
        page_teachers = p.page(page)
        return render(request, 'teachers-list.html', {'teachers': page_teachers,
                                                      'sort': sort,
                                                      'rank_teachers': rank_teachers, })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()
        courses = teacher.course_set.all()
        # 该老师所有课程
        # 或者courses = Course.objects.filter(teacher=teacher)
        has_teacher_fav = False
        has_org_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher_id, fav_type=3):
                has_teacher_fav = True
            elif UserFavorite.objects.filter(user=request.user, fav_id=teacher.org_id, fav_type=2):
                has_org_fav = True
        rank_teachers = Teacher.objects.all().order_by('-click_nums')[:3]
        return render(request, 'teacher-detail.html', {'teacher': teacher,
                                                       'courses': courses,
                                                       'rank_teachers': rank_teachers,
                                                       'has_teacher_fav': has_teacher_fav,
                                                       'has_org_fav': has_org_fav, })
