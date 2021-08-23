# -*- coding: utf-8 -*-
# @Time    : 2021/6/7 16:12
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : response_error_v2.py
# @Software: PyCharm


from rest_framework import status
from rest_framework.response import Response
from django.http.response import JsonResponse


class ServiceError(Exception, Response):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "服务器未知错误"
    default_code = 500

    def __init__(self, errmsg=None, errcode=None, data=None):
        self.errMsg = errmsg or self.default_detail
        self.errCode = errcode or self.default_code
        self.errData = data
        res_data = {
            "code": self.errCode,
            "errmsg": self.errMsg
        }
        if self.errData:
            res_data.setdefault("data", self.errData)
        Response.__init__(self, data=res_data, status=self.status_code)

    @classmethod
    def to_response(cls):
        return JsonResponse(data={"errcode": cls.default_code, "errmsg": cls.default_detail},
                            status=status.HTTP_400_BAD_REQUEST)


class ResponseError(ServiceError):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "未知错误"
    default_code = 400


class ParamMissingError(ResponseError):
    default_detail = "缺少必要参数"
    default_code = 401

    def __init__(self, params=None, errmsg=None, errcode=None, data=None):
        ResponseError.__init__(self, errmsg=errmsg, errcode=errcode, data=data)
        if isinstance(params, str):
            self.data = "缺少的参数：{data}".format(data=params)
        elif isinstance(params, list):
            self.data = "缺少的参数：{data}".format(data="，".join(params))
        else:
            self.data = data


class ParamIllegalError(ResponseError):
    default_detail = "参数不合法"
    default_code = 402

    def __init__(self, params=None, errmsg=None, errcode=None, data=None):
        ResponseError.__init__(self, errmsg=errmsg, errcode=errcode, data=data)
        if isinstance(params, str):
            self.data = "需要修改的参数：{data}".format(data=params)
        elif isinstance(params, list):
            self.data = "需要修改的参数：{data}".format(data="，".join(params))
        else:
            self.data = data


class ResponseUnauthorizedError(ResponseError):
    default_detail = "认证未通过！"
    default_code = 403


class CaptchaWrongError(ResponseError):
    default_detail = "验证码错误！"
    default_code = 404


class CaptchaOverTimeError(ResponseError):
    default_detail = "验证码已经超时失效！"
    default_code = 451


class FrequentError(ResponseError):
    default_detail = "频繁操作！"
    default_code = 405


class MessageSendError(ResponseError):
    default_detail = "短信发送失败"
    default_code = 501


class UserMissError(ResponseError):
    default_detail = "用户已被删除或者不存在"
    default_code = 406


class UserExistError(ResponseError):
    default_detail = "已存在该用户"
    default_code = 407


class UserLoggedError(ResponseError):
    default_detail = "用户已经登录"
    default_code = 408


class UserNotLoggedError(ResponseError):
    default_detail = "用户未登录"
    default_code = 409


class UserLoginInfoError(ResponseError):
    default_detail = "登录信息错误"
    default_code = 410


class UserBannedError(ResponseError):
    default_detail = "该用户已经被封禁！"
    default_code = 440


class UserPermissionError(ResponseError):
    default_detail = "用户无权限！"
    default_code = 441


class VipUpdateError(ResponseError):
    default_detail = "无效的充值选项"
    default_code = 460


class ErrorSelector:
    E400 = ResponseError  # 未知错误
    E401 = ParamMissingError  # 缺少参数
    E402 = ParamIllegalError  # 非法参数错误
    E403 = ResponseUnauthorizedError  # 认证不通过
    E404 = CaptchaWrongError  # 验证码错误
    E405 = FrequentError  # 频繁操作
    E406 = UserMissError  # 用户不存在
    E407 = UserExistError  # 用户已经存在
    E408 = UserLoggedError  # 用户已经登录
    E409 = UserNotLoggedError  # 用户没有登录
    E410 = UserLoginInfoError  # 登录信息错误
    E440 = UserBannedError  # 用户被封禁
    E441 = UserPermissionError  # 用户无权限
    E451 = CaptchaOverTimeError  # 验证码超时
    E460 = VipUpdateError  # 无效的充值选项
    E501 = MessageSendError  # 短信验证码发送失败
