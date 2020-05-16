d = [
    {'title': '首页', 'url': '/login/'}
]

permission_dict = {
    'customer_list': {'id': 1, 'url': '/customer/list/', 'title': '客户列表', 'pid': None, 'pname': None},
    'customer_add': {'id': 2, 'url': '/customer/add/', 'title': '添加客户', 'pid': 1, 'pname': 'customer_list'},
    'customer_edit': {'id': 3, 'url': '/customer/edit/(?P<cid>\\d+)/', 'title': '编辑客户', 'pid': 1,
                      'pname': 'customer_list'},
    'customer_del': {'id': 4, 'url': '/customer/del/(?P<cid>\\d+)/', 'title': '删除客户', 'pid': 1,
                     'pname': 'customer_list'},
    'customer_import': {'id': 5, 'url': '/customer/import/', 'title': '批量导入客户', 'pid': 1,
                        'pname': 'customer_list'}}

for item in permission_dict.values():
    id = item['id']
    pid = item['pid']
    pname = item['pname']

    if pid:
        d.extend([
            {'title': permission_dict[pname]['title'], 'url': permission_dict[pname]['url']},
            {'title': item['title'], 'url': item['url']}
        ])
    else:
        d.extend([
            {'title': item['title'], 'url': item['url']}
        ])

print(d)
"""
[{'title': '首页', 'url': '/login/'},
{'title': '客户列表', 'url': '/customer/list/'},
{'title': '客户列表', 'url': '/customer/list/'}, 
{'title': '添加客户', 'url': '/customer/add/'},
{'title': '客户列表', 'url': '/customer/list/'},
{'title': '编辑客户', 'url': '/customer/edit/(?P<cid>\\d+)/'},
{'title': '客户列表', 'url': '/customer/list/'}, 
{'title': '删除客户', 'url': '/customer/del/(?P<cid>\\d+)/'}, 
{'title': '客户列表', 'url': '/customer/list/'}, 
{'title': '批量导入客户', 'url': '/customer/import/'}]

"""