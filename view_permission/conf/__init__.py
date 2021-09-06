# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 17:24
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : __init__.py.py
# @Software: PyCharm

from view_permission.base.utils import UnionSettings
from view_permission import default_app_settings

settings = UnionSettings(default_app_settings)
