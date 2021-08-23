# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 17:33
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : vpbasepermissioninit.py
# @Software: PyCharm

from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from view_permission.permissions.view import View, Permission
import sys


class Command(BaseCommand):
    help = '初始化权限'

    def handle(self, *args, **options):
        Permission.main()
        self.stdout.write("Success!")
