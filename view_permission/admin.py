from django.contrib import admin
from django.utils.safestring import mark_safe
from view_permission.models import ViewModel, PermissionModel, UserGroup

# Register your models here.

admin.site.register(ViewModel)
admin.site.register(PermissionModel)


class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'view_permissions')}),
    )
    filter_horizontal = ('view_permissions',)
    # filter_vertical = ('view_permissions',)


admin.site.register(UserGroup, UserGroupAdmin)
