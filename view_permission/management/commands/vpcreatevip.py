# -*- coding: utf-8 -*-
# @Time    : 2021/8/20 15:56
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : vpcreatevip.py
# @Software: PyCharm

from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from view_permission.conf import settings
from view_permission.base.utils import VariableNaming
import sys, os


class Command(BaseCommand):
    help = "新建一个VIP"

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            "-n",
            "--name",
        )
        pass

    def handle(self, *args, **options):
        from view_permission.models import UserGroup
        vip_name = options["name"]
        if not vip_name:
            vip_name = input("name:")
        if not vip_name:
            self.stdout("Cancel!")
            return None
        if UserGroup.objects.filter(name=vip_name).exists():
            self.stdout.write("Create VIP failed! The {} already exists!".format(vip_name))
            return None
        UserGroup.objects.create(
            name=vip_name
        )
        sample_path = os.path.join(settings.VIEW_PERMISSION_APP_PATH, "conf", "vip_sample.py")
        with open(sample_path) as f:
            data = f.read()
            data = data.replace("DEFAULT_VIP", VariableNaming.big_camel(vip_name))
            data = data.replace("default_vip", VariableNaming.lower(vip_name))
        self.stdout.write(data)
        self.stdout.write("Success!")
        return None
