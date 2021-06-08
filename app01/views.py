from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01.myforms import MyRegForm
from app01 import models
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F
from utils.page import Pagination


# Create your views here.
def register(request):
    form_obj = MyRegForm()
    if request.method == 'POST':
        # 校验数据是否合法
        form_obj = MyRegForm(request.POST)
        # 判断数据是否合法
        back_dic = {'code': 1000, 'msg': ''}
        if form_obj.is_valid():
            clean_data = form_obj.cleaned_data  # 将数据赋值给对象
            # 删除confirm_password
            clean_data.pop('confirm_password')
            # 用户头像
            file_obj = request.FILES.get('avatar')
            # 判断是否传值
            if file_obj:
                clean_data['avatar'] = file_obj
            # 操作数据库
            models.UserInfo.objects.create_user(**clean_data)
            back_dic['url'] = '/login/'
        else:
            back_dic['code'] = 2000
            back_dic['msg'] = form_obj.errors
        return JsonResponse(back_dic)
    return render(request, 'register.html', locals())


def login(request):
    if request.method == 'POST':
        back_dic = {'code': 1000, 'msg': ''}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = auth.authenticate(request, username=username, password=password)
        if user_obj:
            # 保存用户状态
            auth.login(request, user_obj)
            back_dic['url'] = '/index/'
        else:
            back_dic['code'] = 2000
            back_dic['msg'] = '用户名或密码错误'
        return JsonResponse(back_dic)
    return render(request, 'login.html', locals())


@login_required
def index(request):
    return render(request, 'index.html', locals())


@login_required
def set_password(request):
    back_dic = {'code': 1000, 'msg': ''}
    if request.is_ajax():
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            is_right = request.user.check_password(old_password)
            not_null = len(new_password)
            if not_null:
                if is_right:
                    if new_password == confirm_password:
                        request.user.set_password(new_password)
                        request.user.save()
                        back_dic['msg'] = '修改成功'
                    else:
                        back_dic['code'] = 1001
                        back_dic['msg'] = '两次密码不一致'
                else:
                    back_dic['code'] = 1002
                    back_dic['msg'] = '原密码错误'
            else:
                back_dic['code'] = 1003
                back_dic['msg'] = '密码不能设置为空'
    return JsonResponse(back_dic)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/index/')


def commodity(request):
    commodity_query = models.Commodity.objects.all()
    page_obj = Pagination(current_page=request.GET.get('page'), all_count=commodity_query.count())
    new_commodity_list = commodity_query[page_obj.start:page_obj.end]
    return render(request, 'commodity.html', locals())


def message(request):
    message_query = models.Message.objects.all()
    page_obj = Pagination(current_page=request.GET.get('page'), all_count=message_query.count())
    new_message_list = message_query[page_obj.start:page_obj.end]
    return render(request, 'message.html', locals())


def edit_message(request):
    factory_query = models.Factory.objects.all()
    commodity_query = models.Commodity.objects.all()
    back_dic = {'code': 100, 'msg': ''}
    if request.method == 'POST':
        name = request.POST.get('name')
        count = request.POST.get('count')
        factory_id = request.POST.get('factory')
        type_type = request.POST.get('type')
        unit = request.POST.get('unit')
        person = request.POST.get('person')
        date = request.POST.get('date')
        temp = models.Commodity.objects.filter(pk=name).first()
        if len(name) == 0 or len(count) == 0 or len(factory_id) == 0 or len(type_type) == 0 or len(unit) == 0 or len(
                person) == 0 or len(person) == 0 or len(date) == 0:
            back_dic['code'] = 102
            back_dic['msg'] = '请勿漏填信息!'
        elif temp.count < int(count) and type_type == '0':
            back_dic['code'] = 103
            back_dic['msg'] = '数量不足无法出库!'
        else:
            is_exist = models.F2C.objects.filter(commodity_id=name, factory_id=factory_id)
            if not is_exist:
                models.F2C.objects.create(commodity_id=name, factory_id=factory_id)
            models.Message.objects.create(count=count, factory_id=factory_id, name_id=name, date=date, flag=type_type,
                                          unit=unit, person=person)
            if type_type == '1':
                models.Commodity.objects.filter(pk=name).update(count=F('count') + count)
            elif type_type == '0':
                models.Commodity.objects.filter(pk=name).update(count=F('count') - count)
            back_dic['code'] = 101
        return JsonResponse(back_dic)
    return render(request, 'edit.html', locals())


def search_factory(request):
    factory_query = models.Factory.objects.all()
    page_obj = Pagination(current_page=request.GET.get('page'), all_count=factory_query.count())
    new_commodity_list = factory_query[page_obj.start:page_obj.end]
    return render(request, 'search.html', locals())
