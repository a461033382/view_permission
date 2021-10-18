# -*- coding: utf-8 -*-
# @Time    : 2021/6/21 9:13
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : permission_middleware.py
# @Software: PyCharm

from django.utils.deprecation import MiddlewareMixin
from django.core.handlers.wsgi import WSGIRequest
from view_permission.models import (UserGroup,
                                    PermissionModel,
                                    ViewModel,
                                    UserViewCountModel,
                                    VPUserBaseModel,
                                    VPCacheModel)
from view_permission.permissions.permission import LimitJsonObj, ParamJsonObj, ReqInfoJsonObj
from view_permission.base.vip import NonLogin, BaseUser, SuperUser
from view_permission.base.response_error import *
from view_permission.base.response_error import UserPermissionError
from view_permission.permissions.vip import get_vip_map
from view_permission.conf import settings
from view_permission.base.utils import Utils

from typing import List
from croniter import croniter
from datetime import datetime


class PermissionParamMiddleware(MiddlewareMixin):
    def process_request(self, request: WSGIRequest):
        pass

    def process_view(self, request: WSGIRequest, callback, callback_args, callback_kwargs):
        user_group = self.get_group(request)
        view_name = request.resolver_match.view_name  # type:str
        view_name = view_name.split(":")[-1]
        request.vp_info = {}

        permission_list = user_group.get_permission(view_name=view_name,
                                                    method=request.method)  # type:List[PermissionModel]
        param_list = request.GET.dict()
        param_list.update(request.POST.dict())
        permission_list = permission_list or []
        for permission in permission_list:
            if permission.need_login and isinstance(user_group, NonLogin):  # 确认是否需要登录
                return UserNotLoggedError.to_response()
            obj = LimitJsonObj.from_json_str(permission.param_json)
            request.vp_info.update(ReqInfoJsonObj.from_json_str(permission.req_info).req_info)
            if not obj(**param_list):
                return UserPermissionError.to_response()

    def process_response(self, request: WSGIRequest, response: Response):
        return response

    def get_group(self, request: WSGIRequest):
        if hasattr(request, "user"):
            user = request.user  # type:VPUserBaseModel
            if user.is_superuser:
                return SuperUser()
            if not isinstance(user, VPUserBaseModel):
                return NonLogin()
            return (get_vip_map().get(user.view_group.name) or BaseUser)()


class PermissionCountMiddleware(MiddlewareMixin):

    def process_request(self, request: WSGIRequest):
        pass

    def process_view(self, request: WSGIRequest, callback, callback_args, callback_kwargs):

        self.reset_check()

        user = getattr(request, "user")
        user_group = self.get_group(request)
        view_name = request.resolver_match.view_name  # type:str
        view_name = view_name.split(":")[-1]
        method = request.method
        method = method.upper()
        method_num = ViewModel.request_method_dict_T[method]
        view_obj = ViewModel.objects.filter(view=view_name, method=method_num).first()
        request.vp_info = {}

        permission_list = user_group.get_permission(view_name=view_name,
                                                    method=request.method)  # type:List[PermissionModel]
        param_list = request.GET.dict()
        param_list.update(request.POST.dict())
        permission_list = permission_list or []
        for permission in permission_list:
            call_limit = permission.call_limit
            if call_limit != -1 and isinstance(user, VPUserBaseModel):
                call_time = UserViewCountModel.get_call_time(user, view=permission.view)
                if call_time >= call_limit:
                    return CallLimitError.to_response()
        if view_obj:
            UserViewCountModel.add_call_time(user, view_obj)

    def get_group(self, request: WSGIRequest):
        if hasattr(request, "user"):
            user = request.user  # type:VPUserBaseModel
            if user.is_superuser:
                return SuperUser()
            if not isinstance(user, VPUserBaseModel):
                return NonLogin()
            return (get_vip_map().get(user.view_group.name) or BaseUser)()

    def reset_check(self):
        reset_time = VPCacheModel.get_cache_by_key(settings.NEXT_RESET_TIME_CACHE_KEY)
        reset_time = Utils.is_datetime(reset_time)
        if not reset_time or datetime.now() > reset_time:
            UserViewCountModel.reset()
            next_time = croniter(settings.CALL_LIMIT_CRON).next(datetime)
            VPCacheModel.add_cache(key=settings.NEXT_RESET_TIME_CACHE_KEY,
                                   value=next_time, auto_update=True)
