# -*- coding: utf-8 -*-
# @Time    : 2021/8/23 13:54
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : vpremovevip.py
# @Software: PyCharm

from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from view_permission.conf import settings
from view_permission.base.utils import VariableNaming
import sys, os


class Command(BaseCommand):
    help = '删除一个VIP'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            "-n",
            "--name",
        )

    def handle(self, *args, **options):
        from view_permission.models import UserGroup
        vip_name = options["name"]
        if not vip_name:
            vip_name = input("name:")
        if not vip_name:
            self.stdout("Cancel!")
            return None
        if not UserGroup.objects.filter(name=vip_name).exists():
            self.stdout.write("Remove VIP failed! The {} is not exist!".format(vip_name))
            return None
        res = input("这是一个不可逆操作，请确认操作。Y/n：")
        if res.lower() != "y":
            self.stderr.write("操作被取消！")
        vip = UserGroup.objects.filter(name=vip_name).first()  # type:UserGroup
        vip.delete()
        self.stdout.write("Success!")
        return None
