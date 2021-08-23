# -*- coding: utf-8 -*-
# @Time    : 2021/8/23 14:04
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : vpremoveallvip.py
# @Software: PyCharm


from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from view_permission.conf import settings
from view_permission.base.utils import VariableNaming
import sys, os


class Command(BaseCommand):
    help = '删除所有VIP'

    def handle(self, *args, **options):
        from view_permission.models import UserGroup
        vip = UserGroup.objects.all()
        res = input("这是一个不可逆操作，请确认操作。Y/n：")
        if res.lower() != "y":
            self.stderr.write("操作被取消！")
        vip.delete()
        self.stdout.write("Success!")
        return None
