# -*- coding: utf-8 -*-
# @Time    : 2021/9/8 10:26
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : vp_type.py
# @Software: PyCharm

from view_permission.permissions.vp_type import VPType


class VPStr(VPType):
    name = "str"
    target_type = str


class VPInt(VPType):
    name = "int"
    target_type = int


class VPFloat(VPType):
    name = "float"
    target_type = float


class VPList(VPType):
    name = "list"
    target_type = list

    @classmethod
    def _validate(cls, value: str):
        if value[0] != "[" or value[-1] != "]":
            return False
        return True

    @classmethod
    def change(cls, value: str):
        return value[1:-1].split(",")
