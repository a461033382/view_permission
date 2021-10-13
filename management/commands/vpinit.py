# -*- coding: utf-8 -*-
# @Time    : 2021/8/19 9:18
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : vpinit.py
# @Software: PyCharm

from django.core.management import BaseCommand


class Command(BaseCommand):
    help = '初始化权限'

    def handle(self, *args, **options):
        from view_permission.permissions.view import View, Permission
        res = View.main()
        if res:
            self.stdout.write("Success!")
