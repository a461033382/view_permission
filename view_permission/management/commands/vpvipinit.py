# -*- coding: utf-8 -*-
# @Time    : 2021/9/1 14:19
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : vpvipinit.py
# @Software: PyCharm

from django.core.management import BaseCommand
from view_permission.conf import settings
from typing import List
import importlib

from view_permission.permissions.vip import VipBaseClass, VipMap


class Command(BaseCommand):
    help = 'VIP初始化'

    def handle(self, *args, **options):
        cls_obj_list = self.get_cls_from_path()
        for cls_obj in cls_obj_list:
            res = cls_obj.to_db()
            if res:
                self.stdout.write("VIP {} 添加成功！".format(cls_obj.name))
        self.stdout.write("Success!")

    @staticmethod
    def get_cls_from_path() -> List[VipBaseClass]:
        return VipMap.values()
