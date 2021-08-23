# -*- coding: utf-8 -*-
# @Time    : 2021/8/23 15:16
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : vprunserver.py
# @Software: PyCharm

from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from view_permission.conf import settings as vp_settings
from django.conf import settings as django_settings
from view_permission.base.utils import VariableNaming
import sys, os


class Command(BaseCommand):
    help = '启动vp服务器'

    def add_arguments(self, parser: CommandParser):
        parser.add_argument(
            "-n",
            "--name",
        )

    def handle(self, *args, **options):
        from view_permission.html.run import run
        from django.conf import settings as django_settings
        run(django_settings.BASE_DIR, os.environ.get("DJANGO_SETTINGS_MODULE"))
