from django.conf import settings


def init_permission(request, obj):
    """
    权限和菜单信息初始化，以后使用时，需要在登陆成功后调用该方法将权限和菜单信息放入session
    :return:
    """
    # 获取用户信息和权限信息写入 session 中
    permission_queryset = obj.roles.filter(permissions__url__isnull=False). \
        values('permissions__url',
               'permissions__is_menu',
               'permissions__title',
               'permissions__icon').distinct()

    """
    <QuerySet [{'permissions__url': '/customer/list/', 'permissions__is_menu': False, 'permissions__title': '客户列表', 'permissions__icon': None},
     {'permissions__url': '/customer/add/', 'permissions__is_menu': False, 'permissions__title': '添加客户', 'permissions__icon': None}, 
     {'permissions__url': '/customer/edit/(?P<cid>\\d+)/', 'permissions__is_menu': False, 'permissions__title': '编辑客户', 'permissions__icon': None}, {'permissions__url': '/customer/del/(?P<cid>\\d+)/', 
     'permissions__is_menu': False, 'permissions__title': '删除客户', 'permissions__icon': None},
      {'permissions__url': '/customer/import/', 'permissions__is_menu': False, 'permissions__title': '批量导入客户', 'permissions__icon': None}]>
    """

    # 获取菜单列表、权限列表，分别存入 session 中
    menu_list = []
    permission_list = []

    print(permission_queryset)

    for item in permission_queryset:
        # 权限
        permission_list.append({'permissions__url': item['permissions__url']})

        # 菜单
        if item['permissions__is_menu']:
            menu_list.append({
                'title': item['permissions__title'], 'icon': item['permissions__icon'], 'url': item['permissions__url']
            })

    print('menu_list==>', menu_list)
    print('permission_list==>', permission_list)

    request.session[settings.MENU_SESSION_KEY] = menu_list
    request.session[settings.PERMISSION_SESSION_KEY] = permission_list

