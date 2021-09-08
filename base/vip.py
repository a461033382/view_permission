# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 15:08
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : vip.py
# @Software: PyCharm

from view_permission.permissions.vip import VipBaseClass
from view_permission.conf import settings


class NonLogin(VipBaseClass):
    name = settings.NON_LOGIN_NAME


class BaseUser(VipBaseClass):
    name = settings.BASE_VIP_NAME


class SuperUser(VipBaseClass):
    name = settings.SUPER_USER_NAME

    def get_model(self):
        return True

    def get_permission(self, view_name: str, method: str):
        return None

    def get_all_permission(self):
        return None


VipMap = {
    "NON_LOGIN": NonLogin,
    "BASE_USER": BaseUser,
    "SUPER_USER": SuperUser
}
