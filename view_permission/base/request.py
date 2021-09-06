# -*- coding: utf-8 -*-
# @Time    : 2021/9/6 9:45
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : request.py
# @Software: PyCharm

from rest_framework.request import Request


class VPRequest(Request):

    def __init__(self, vp_info=None, *args, **kwargs):
        self.vp_info = vp_info or {}
        Request.__init__(*args, **kwargs)

    @classmethod
    def from_request(cls, request: Request):
        pass
