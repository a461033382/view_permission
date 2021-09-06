from django.apps import AppConfig
# from django.conf import settings
from django.urls import URLPattern, URLResolver
from django.db import transaction
from view_permission.conf import settings


class ViewlistConfig(AppConfig):
    name = 'view_permission'

    def ready(self):
        if not settings.DEBUG:
            from view_permission.permissions.view import View, Permission
            View.main()
            Permission.main()
