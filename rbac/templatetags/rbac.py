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
    menu_list = request.session.get(settings.MENU_SESSION_KEY)

    for item in menu_list:
        reg = "^%s$" % item['url']

        # 给当前选中菜单添加选中样式
        if re.match(reg, request.path_info):
            item['class'] = 'active'  # 添加一个新的 class 熟悉

    return {'menu_list': menu_list}
