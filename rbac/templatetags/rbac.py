from collections import OrderedDict

from django.template import Library
from django.conf import settings
import re

register = Library()


@register.inclusion_tag('rbac/menu.html')
def menu(request):
    """
    生成菜单
    :param request:
    :return:
    """
    menu_dict = request.session.get(settings.MENU_SESSION_KEY)
    """
    {'2': {'title': '客户管理', 'icon': 'fa-clipboard', 
    'children': [{'id': 1, 'title': '客户列表', 'url': '/customer/list/'}]}}
    """

    ordered_dict = OrderedDict()
    for item in sorted(menu_dict):
        ordered_dict[item] = menu_dict[item]
        menu_dict[item]['class'] = 'hide'

        for node in menu_dict[item]['children']:
            if request.current_menu_id == node['id']:
                node['class'] = 'active'
                menu_dict[item]['class'] = ''

    """
    {'2': {'title': '客户管理', 'icon': 'fa-clipboard', 'children':
     [{'id': 1, 'title': '客户列表', 'url': '/customer/list/', 'class': 'active'}], 'class': ''}}
    """
    return {'menu_dict': ordered_dict}


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    """面包屑导航"""

    return {'breadcrumb_list': request.breadcrumb_list}


@register.filter
def has_permission(request, name):
    """是否有权限"""
    permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
    if name in permission_dict:
        return True
