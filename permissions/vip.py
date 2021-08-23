# -*- coding: utf-8 -*-
# @Time    : 2021/7/23 14:48
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : vip.py
# @Software: PyCharm

from view_permission.models import UserGroup


class VipBaseClass(object):
    name = None

    @classmethod
    def get_model(cls):
        assert cls.name, "未输入VIP名"
        obj = UserGroup.objects.filter(name=cls.name).first()
        assert obj, "未找到该VIP名：{}".format(cls.name)
        setattr(cls, "obj", obj)
        return obj

    @classmethod
    def get_all_permission(cls):
        view_permissions = cls.get_model().view_permissions.all()
        return view_permissions

    @classmethod
    def get_permission(cls, view_name: str, method: str):
        view_permissions = [i for i in cls.get_all_permission() if
                            i.view.view == view_name and
                            i.view.get_method_display() == method]
        return view_permissions

    def __str__(self):
        return self.__class__.__name__


class NonLogin(VipBaseClass):
    name = "NON_LOGIN"


class SuperUser(VipBaseClass):
    name = "SuperUser"

    def get_model(self):
        return True

    def get_permission(self, view_name: str, method: str):
        return None

    def get_all_permission(self):
        return None


VipMap = {
    "NON_LOGIN": NonLogin,
}
