# -*- coding: utf-8 -*-
# @Time    : 2021/4/29 15:11
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : response_error.py
# @Software: PyCharm

from rest_framework.status import *
from rest_framework.response import Response


class SuccessResponse(Response):
    def __init__(self, data=None):
        d = {
            "code": 200,
            "info": "OK"
        }
        if data:
            d.setdefault("data", data)
        Response.__init__(self, data=d, status=HTTP_200_OK)


class DebugResponse(Response):
    def __init__(self, data=None):
        d = {
            "code": 200,
            "info": "施工中"
        }
        if data:
            d["data"] = data
        Response.__init__(self, data=d, status=HTTP_200_OK)
