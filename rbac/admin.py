from django.contrib import admin

from .models import Permission, UserInfo, Role


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'is_menu', 'icon']
    list_editable = ['url']


admin.site.register(Permission, PermissionAdmin)

admin.site.register(Role)


class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'roles']

    def roles(self, obj):

        return [i.title for i in obj.roles.all()]

admin.site.register(UserInfo, UserAdmin)

