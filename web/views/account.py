from django.conf import settings
from django.shortcuts import render, redirect

from rbac import models
from rbac.service.init_permission import init_permission


def login(request):
    """登录"""
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        # 获取用户名、密码
        username = request.POST.get('username')
        pwd = request.POST.get('password')

        # 校验是否合法
        obj = models.UserInfo.objects.filter(name=username, password=pwd).first()
        if not obj:
            return render(request, 'login.html', {'msg': '用户名或密码错误'})

        # 将用户信息写入 session
        request.session['user_info'] = {'id': obj.id, 'name': obj.name}
        init_permission(request, obj)   # 权限校验

        return redirect('/customer/list/')
