import re

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class RbacMiddleware(MiddlewareMixin):
    """
    权限控制中间件
    """

    def process_request(self, request):
        # 当前请求 URL
        current_url = request.path_info

        # 处理白名单
        for reg in settings.VALID_URL:
            if re.match(reg, current_url):
                return None

        # 获取用户所以权限
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_dict:
            return redirect('/login/')

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

        # 面包屑导航，request 中赋值
        request.breadcrumb_list = [
            {'title': '首页', 'url': '/'}
        ]

        # 权限校验
        flag = False
        for item in permission_dict.values():
            # 'customer_add': {'id': 2, 'url': '/customer/add/', 'title': '添加客户', 'pid': 1, 'pname': 'customer_list'},
            id = item['id']         # 2
            pid = item['pid']       # 1
            pname = item['pname']   # customer_list
            reg = "^%s$" % item.get('url')
            if re.match(reg, current_url):
                flag = True

                # pid 为 None，表示是用来菜单的权限，否则不能做菜单
                if pid:
                    # 若有 pid，则当前点击的菜单ID，即为当前菜单的 pid，比如点击 "添加客户，那么他的 pid 为 客户列表"
                    request.current_menu_id = pid
                    request.breadcrumb_list.extend([
                        {'title': permission_dict[pname]['title'], 'url': permission_dict[pname]['url']},
                        {'title': item['title'], 'url': item['url']},
                    ])
                else:
                    # 没有 pid，那么当前点击菜单即为自身
                    request.current_menu_id = id
                    request.breadcrumb_list.extend([
                        {'title': item['title'], 'url': item['url']}
                    ])

                break

        if not flag:
            return HttpResponse('无权访问')
