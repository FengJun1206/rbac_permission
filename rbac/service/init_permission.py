from django.conf import settings


def init_permission(request, obj):
    """
    权限和菜单信息初始化，以后使用时，需要在登陆成功后调用该方法将权限和菜单信息放入session
    :return:
    """
    # 获取用户信息和权限信息写入 session 中
    permission_queryset = obj.roles.filter(permissions__url__isnull=False).values(
        'permissions__id',
        'permissions__url',
        'permissions__title',
        'permissions__name',
        'permissions__parent_id',
        'permissions__parent__name',
        'permissions__menu_id',
        'permissions__menu__title',
        'permissions__menu__icon',
    ).distinct()

    # 获取菜单列表、权限列表，分别存入 session 中
    menu_dict = {}
    permission_dict = {}

    """
    <QuerySet [{'permissions__id': 1, 'permissions__url': '/customer/list/', 'permissions__title': '客户列表', 
    'permissions__name': 'customer_list', 'permissions__parent_id': None, 'permissions__parent__name': None, 
    'permissions__menu_id': 2, 'permissions__menu__title': '客户管理', 'permissions__menu__icon': 'fa-clipboard'}, 
    {'permissions__id': 2, 'permissions__url': '/customer/add/', 'permissions__title': '添加客户', 
    'permissions__name': 'customer_add', 'permissions__parent_id': 1, 'permissions__parent__name': 'customer_list', 
    'permissions__menu_id': None, 'permissions__menu__title': None, 'permissions__menu__icon': None}, {'permissions__id': 3,
    'permissions__url': '/customer/edit/(?P<cid>\\d+)/', 'permissions__title': '编辑客户', 'permissions__name': 'customer_edit', 
    'permissions__parent_id': 1, 'permissions__parent__name': 'customer_list', 'permissions__menu_id': None, 
    'permissions__menu__title': None, 'permissions__menu__icon': None}, {'permissions__id': 4, 'permissions__url': '/customer/del/(?P<cid>\\d+)/', 
    'permissions__title': '删除客户', 'permissions__name': 'customer_del', 'permissions__parent_id': 1,
     'permissions__parent__name': 'customer_list', 'permissions__menu_id': None, 'permissions__menu__title': None, 
     'permissions__menu__icon': None}, {'permissions__id': 5, 'permissions__url': '/customer/import/', 
     'permissions__title': '批量导入客户', 'permissions__name': 'customer_import', 'permissions__parent_id': 1,
      'permissions__parent__name': 'customer_list', 'permissions__menu_id': None, 'permissions__menu__title': None, 
      'permissions__menu__icon': None}]>

    """

    for item in permission_queryset:
        # 权限
        permission_dict[item['permissions__name']] = {
            'id': item['permissions__id'],
            'url': item['permissions__url'],
            'title': item['permissions__title'],
            'pid': item['permissions__parent_id'],
            'pname': item['permissions__parent__name']
        }

        # 菜单
        menu_id = item.get('permissions__menu_id')
        # 没有 menu_id，说明不用显示在菜单栏
        if not menu_id:  # 若没有 menu_id，则停止当前循环，继续下一次循环
            continue

        # 若没在字典中，表示是新的菜单
        if menu_id not in menu_dict:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'children': [
                    {
                        'id': item['permissions__id'],
                        'title': item['permissions__title'],
                        'url': item['permissions__url']
                    }
                ]
            }
        else:
            # 若有，则添加子菜单
            menu_dict[menu_id]['children'].append({
                'id': item['permissions__id'],
                'title': item['permissions__title'],
                'url': item['permissions__url']
            })

    # print('menu_dict==>', menu_dict)
    # print('permission_dict==>', permission_dict)

    """
    menu_dict==> {2: {'title': '客户管理', 'icon': 'fa-clipboard', 
    'children': [{'id': 1, 'title': '客户列表', 'url': '/customer/list/'}]}}
    """

    """
    permission_dict==> {
    'customer_list': {'id': 1, 'url': '/customer/list/', 'title': '客户列表', 'pid': None, 'pname': None}, 
    'customer_add': {'id': 2, 'url': '/customer/add/', 'title': '添加客户', 'pid': 1, 'pname': 'customer_list'},
      'customer_edit': {'id': 3, 'url': '/customer/edit/(?P<cid>\\d+)/', 'title': '编辑客户', 'pid': 1, 'pname': 'customer_list'}, 
     'customer_del': {'id': 4, 'url': '/customer/del/(?P<cid>\\d+)/', 'title': '删除客户', 'pid': 1,
      'pname': 'customer_list'},
    'customer_import': {'id': 5, 'url': '/customer/import/', 'title': '批量导入客户', 'pid': 1,
       'pname': 'customer_list'}}

    """

    request.session[settings.MENU_SESSION_KEY] = menu_dict
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
