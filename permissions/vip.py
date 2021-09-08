# -*- coding: utf-8 -*-
# @Time    : 2021/7/23 14:48
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : vip.py
# @Software: PyCharm

from view_permission.models import UserGroup
from view_permission.conf import settings
from view_permission.base.utils import MapClass
from typing import List
import importlib


class VipBaseClass(MapClass):

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

    @classmethod
    def to_db(cls):
        assert cls.name, "未输入VIP名"
        obj = UserGroup.objects.filter(name=cls.name).first()
        if obj:
            return False
        UserGroup.objects.create(
            name=cls.name
        )
        return True

    def __str__(self):
        return self.__class__.__name__


def get_vip_map() -> dict:
    vip_map = {}
    vip_cls_list = []
    vip_path_list = tuple(settings.BASE_VIP_DIR + settings.VIP_DIR)  # type:List[str]
    for vip_path in vip_path_list:
        vip_path_obj = importlib.import_module(vip_path)
        cls_list = [getattr(vip_path_obj, i) for i in vip_path_obj.__dict__]
        cls_list = [i for i in cls_list if
                    isinstance(i, type) and i != VipBaseClass and issubclass(i, VipBaseClass)]
        vip_cls_list += cls_list
    vip_cls_list = list(tuple(vip_cls_list))
    for i in vip_cls_list:
        if vip_map.get(i.name):
            raise Exception("错误！ {}类 和 {}类 指向的VIP名一致".format(i.__name__, vip_map[i.name].__name__))
        vip_map[i.name] = i
    return vip_map


VipMap = get_vip_map()

if __name__ == '__main__':
    a = VipBaseClass.get_class_map(settings.BASE_VIP_DIR)
