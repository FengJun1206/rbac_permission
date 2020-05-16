from django.contrib import admin

from .models import Permission, UserInfo, Role, Menu


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'name', 'parent', 'menu']
    list_editable = ['url']


admin.site.register(Permission, PermissionAdmin)
admin.site.register(Menu)
admin.site.register(Role)


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'roles']

    def roles(self, obj):

        return [i.title for i in obj.roles.all()]

admin.site.register(UserInfo, UserAdmin)

