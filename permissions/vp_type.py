# -*- coding: utf-8 -*-
# @Time    : 2021/9/8 9:48
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : vp_type.py
# @Software: PyCharm

from typing import List, Dict
from view_permission.base.utils import MapClass


class VPType(MapClass):
    target_type = None  # type:type

    def __new__(cls, value):
        return cls._change(value)

    @classmethod
    def get_class_map(cls: type, path_list: List[str] = None):
        path_list = path_list or []
        return MapClass.get_class_map(["view_permission.base.vp_type"] + path_list)

    @classmethod
    def _check(cls):
        if not cls.name or not cls.target_type:
            return False
        return True

    @classmethod
    def _validate(cls, value: str):
        try:
            cls.target_type(value)
        except Exception as e:
            return False
        return True

    @classmethod
    def _change(cls, value: str):
        if not isinstance(value, str):
            return value
        if not cls._check():
            return value
        if not cls._validate(value):
            return value
        return cls.change(value)

    @classmethod
    def change(cls, value):
        return cls.target_type(value)
