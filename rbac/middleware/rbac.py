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
        permission_list = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_list:
            return redirect('/login/')

        """
        [{'permissions__url': '/customer/list/'}, {'permissions__url': '/customer/add/'},
         {'permissions__url': '/customer/edit/(?P<cid>\\d+)/'}, 
         {'permissions__url': '/customer/del/(?P<cid>\\d+)/'},
          {'permissions__url': '/customer/import/'}]
        """

        # 权限校验
        flag = False
        for item in permission_list:
            reg = "^%s$" % item.get('permissions__url')
            if re.match(reg, current_url):
                flag = True
                break

        if not flag:
            return HttpResponse('无权访问')
