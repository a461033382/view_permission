# -*- coding: utf-8 -*-
# @Time    : 2021/6/21 9:13
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : permission_middleware.py
# @Software: PyCharm

from django.utils.deprecation import MiddlewareMixin
from django.middleware.common import CommonMiddleware
from django.middleware.csrf import CsrfViewMiddleware
from django.core.handlers.wsgi import WSGIRequest
from rest_framework.response import Response
from django.http.response import HttpResponse, JsonResponse
from django.contrib.auth.models import AnonymousUser
from view_permission.models import UserGroup, PermissionModel, ViewModel
from view_permission.permissions.permission import LimitJsonObj, ParamJsonObj
from apps.user.models import UserModel
from view_permission.permissions.vip import NonLogin, Vip1, Vip2, VipMap, SuperUser
from view_permission.base.response_error import *
from view_permission.base.response_error import UserPermissionError

from typing import List


class PermissionParamMiddleware(MiddlewareMixin):
    def process_request(self, request: WSGIRequest):
        pass

    def process_view(self, request: WSGIRequest, callback, callback_args, callback_kwargs):
        user_group = self.get_group(request)
        view_name = request.resolver_match.view_name
        permission_list = user_group.get_permission(view_name=view_name,
                                                    method=request.method)  # type:List[PermissionModel]
        param_list = request.GET.dict()
        param_list.update(request.POST.dict())
        permission_list = permission_list or {}
        for permission in permission_list:
            obj = LimitJsonObj.from_json_str(permission.param_json)
            if not obj(**param_list):
                if isinstance(user_group, NonLogin):
                    return UserNotLoggedError.to_response()
                return UserPermissionError.to_response()

    def process_response(self, request: WSGIRequest, response: Response):
        return response

    def get_group(self, request: WSGIRequest):
        if hasattr(request, "user"):
            user = request.user  # type:UserModel
            if user.is_superuser or user.is_staff:
                return SuperUser()
            if not isinstance(user, UserModel):
                return NonLogin()
            return VipMap.get(user.view_group.name)() or Vip1()


class PermissionCountMiddleware(MiddlewareMixin):

    def process_request(self, request: WSGIRequest):
        # print(request)
        pass

    def process_view(self, request: WSGIRequest, callback, callback_args, callback_kwargs):
        # print(request)
        pass

    pass
