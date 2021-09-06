# -*- coding: utf-8 -*-
# @Time    : 2021/6/18 14:39
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : view.py
# @Software: PyCharm

from django.apps import AppConfig
from view_permission.conf import settings
from django.urls import URLPattern, URLResolver
from django.db import transaction
from view_permission.models import ViewModel

import os, django


# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "guild_rank.settings")
# django.setup()


class View(object):

    @staticmethod
    def get_view_class():
        apps_dict = {}
        urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
        url_patterns = urlconf.urlpatterns  # type:list
        for i in url_patterns:
            if i.app_name not in settings.BASE_EXCLUDE_APP_NAMES + settings.EXCLUDE_APP_NAMES:
                for v in i.reverse_dict.keys():
                    if hasattr(v, "view_class"):
                        apps_dict["{}.{}".format(v.view_class.__module__, v.__name__)] = v
        return apps_dict

    @staticmethod
    def get_view_url(base_dir=None, url_patterns: URLResolver = None):
        base_dir = base_dir or ""
        url_dict = {}
        if url_patterns:
            base_dir = base_dir + str(url_patterns.pattern)
            url_patterns = url_patterns.url_patterns
        else:
            urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])
            url_patterns = urlconf.urlpatterns  # type:list
        for url_obj in url_patterns:
            if isinstance(url_obj, URLResolver):
                url_dict = dict(url_dict, **View.get_view_url(base_dir, url_patterns=url_obj))
            elif isinstance(url_obj, URLPattern):
                pattern = url_obj.pattern
                url = "{}{}".format(base_dir, pattern)
                url_dict[url_obj.lookup_str] = url
        return url_dict

    @staticmethod
    def view_to_database(view_dict, view_url_dict):
        view_str_list = list(view_dict.keys())
        for view_str in view_str_list:
            view_obj = view_dict[view_str]
            view_url = view_url_dict.get(view_str)
            if not view_url:
                continue
            http_method_names = set(view_obj.view_class.http_method_names) & set(
                [i.lower() for i in settings.HTTP_METHOD_NAMES])
            method_list = set(i.lower() for i in http_method_names)
            allowed_method_list = [i.lower() for i in ViewModel.request_method_dict.values()]
            method_list = [i for i in method_list if i in allowed_method_list]
            try:
                with transaction.atomic():
                    all_model_obj_list = ViewModel.objects.filter(url=view_url)
                    for _ in all_model_obj_list:
                        _.is_active = False
                        _.save()
                    for method in method_list:
                        method = method.upper()
                        method_num = ViewModel.request_method_dict_T[method]
                        view_model_obj = ViewModel.objects.filter(url=view_url,
                                                                  method=method_num).first()  # type:ViewModel
                        if view_model_obj:
                            # 已经存在的RUL
                            view_model_obj.is_active = True
                            view_model_obj.view = view_str or view_model_obj.view
                        else:
                            # 新的URL
                            view_model_obj = ViewModel(
                                view=view_str,
                                name="{} {}".format(view_obj.__name__, method.upper()),
                                url=view_url,
                                method=method_num
                            )
                        view_model_obj.save()
            except Exception as e:
                raise Exception("更新view失败！ 错误原因：{}".format(e.args))

    @staticmethod
    def main():
        view_dict = View.get_view_class()
        view_url_dict = View.get_view_url()
        View.view_to_database(view_dict, view_url_dict)
        return True


class Permission(object):

    @staticmethod
    def _create_default_permission(view_obj):
        from view_permission.models import ViewModel, PermissionModel
        if not isinstance(view_obj, ViewModel):
            raise TypeError("view_obj is not ViewModel class!")
        default_permission_obj = PermissionModel.objects.filter(
            view=view_obj
        ).first()
        if not default_permission_obj:
            permission_name = "{view} {method} {word}".format(
                view=view_obj.view,
                method=view_obj.get_method_display(),
                word="BASE"
            )
            print("添加一个新的权限：{}".format(permission_name))
            default_permission_obj = PermissionModel(
                name=permission_name,
                view=view_obj
            )
        default_permission_obj.save()
        return True

    @staticmethod
    def main():
        from view_permission.models import ViewModel
        print("更新默认权限")
        all_view_obj = ViewModel.objects.all()
        try:
            with transaction.atomic():
                for view_obj in all_view_obj:
                    Permission._create_default_permission(view_obj)
        except Exception as e:
            raise Exception("更新默认权限失败")


if __name__ == '__main__':
    print(View.main())
