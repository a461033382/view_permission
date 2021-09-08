# -*- coding: utf-8 -*-
# @Time    : 2021/8/18 15:57
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : utils.py
# @Software: PyCharm

import datetime
from dateutil.relativedelta import relativedelta
from importlib import import_module
from django.conf import settings
from django.conf import Settings

import importlib
import os
import time
import warnings
import importlib
from pathlib import Path
from typing import List

from django.conf import global_settings, ENVIRONMENT_VARIABLE
from django.core.exceptions import ImproperlyConfigured
from django.utils.deprecation import (
    RemovedInDjango30Warning, RemovedInDjango31Warning,
)
import os


class Utils:
    @staticmethod
    def get_week(date: datetime.date = None):
        """
        :param date: date对象，获取该对象所在的星期数，默认为今天
        :return:Int类型，从1开始的周数
        """
        date = date or datetime.date.today()
        res = date.strftime("%W")
        return int(res)

    @staticmethod
    def get_week_time(week: int, year=None):
        if week not in range(1, 53):
            raise ValueError("周数取值范围：1-52")
        year = year or datetime.date.today().year
        year_start = datetime.date(year=year, month=1, day=1)
        if year_start.isoweekday() != 1:
            year_start += datetime.timedelta(days=7 - year_start.weekday())
        return year_start + datetime.timedelta(weeks=week - 1)

    @staticmethod
    def is_int(s: str):
        try:
            num = int(s)
        except Exception as e:
            return False
        return num

    @staticmethod
    def is_float(s: str):
        try:
            num = float(s)
        except Exception as e:
            return False
        return num

    @classmethod
    def is_num(cls, s: str):
        num = cls.is_int(s)
        if isinstance(num, int):
            return num
        num = cls.is_float(s)
        if isinstance(num, float):
            return num
        else:
            return False

    @staticmethod
    def is_date(s: str, format: str = "%Y-%m-%d"):
        try:
            res = datetime.datetime.strptime(s, format)
            res = res.date()
        except Exception as e:
            return False
        return res

    @staticmethod
    def get_date_from_date_type(date_type: str):
        date_map = {
            "today": datetime.date.today(),
            "yesterday": datetime.date.today() - 1 * datetime.timedelta(days=1),
            "monday": datetime.date.today() - datetime.date.today().weekday() * datetime.timedelta(days=1),
            "month_first_day": datetime.date.today().replace(day=1),
            "year_first_day": datetime.date.today().replace(month=1, day=1)
        }

        def today():
            start_date = date_map["today"]
            end_date = date_map["today"]
            return start_date, end_date

        def yesterday():
            end_date = date_map["yesterday"]
            start_date = date_map["yesterday"]
            return start_date, end_date

        def days_7():
            end_date = date_map["yesterday"]
            start_date = end_date - relativedelta(days=7)
            return start_date, end_date

        def days_15():
            end_date = date_map["yesterday"]
            start_date = end_date - relativedelta(days=15)
            return start_date, end_date

        def days_30():
            end_date = date_map["yesterday"]
            start_date = end_date - relativedelta(days=30)
            return start_date, end_date

        def week():
            end_date = date_map["monday"] - relativedelta(days=1)
            start_date = end_date - relativedelta(weeks=1, days=-1)
            return start_date, end_date

        def month():
            end_date = date_map["month_first_day"] - relativedelta(days=1)
            start_date = end_date - relativedelta(months=1, days=-1)
            return start_date, end_date

        func_map = dict(
            today=today,
            yesterday=yesterday,
            days_7=days_7,
            days_15=days_15,
            days_30=days_30,
            week=week,
            month=month
        )
        if date_type not in func_map:
            return {"status": False}
        start_date, end_date = func_map[date_type]()
        return {"status": True,
                "date": (start_date, end_date)}

    @staticmethod
    def get_start_date_and_end_date(date_type: str,
                                    start_date: datetime.date or str = None,
                                    end_date: datetime.date or str = None,
                                    format: str = "%Y-%m-%d"):
        date_dict = Utils.get_date_from_date_type(date_type)
        if date_dict["status"]:
            start_date, end_date = date_dict["date"]
            return start_date, end_date
        if isinstance(start_date, str):
            start_date = Utils.is_date(start_date, format)
        if isinstance(end_date, str):
            end_date = Utils.is_date(end_date, format)
        if not isinstance(start_date, datetime.date) or not isinstance(end_date, datetime.date):
            return None, None
        return start_date, end_date

    @staticmethod
    def date2datetime(d: datetime.date, h: int = 0, m: int = 0, s: int = 0):
        if h not in range(0, 24):
            h = 0
        if m not in range(0, 60):
            m = 0
        if s not in range(0, 60):
            s = 0
        return datetime.datetime(d.year, d.month, d.day, h, m, s)

    @staticmethod
    def get_user_model():
        model_str = settings.AUTH_USER_MODEL
        UserModel = import_module(model_str)
        return UserModel


class VariableNaming(object):

    @classmethod
    def big_camel(cls, variable_str: str):
        variable_str = variable_str.lower()
        a_list = variable_str.split("_")
        a_list = [i.capitalize() for i in a_list]
        return "".join(a_list)

    @classmethod
    def little_camel(cls, variable_str: str):
        variable_str = variable_str.lower()
        a_list = variable_str.split("_")
        a_list = [i.capitalize() for i in a_list]
        a_list[0] = a_list[0].lower()
        return "".join(a_list)

    @classmethod
    def upper(cls, variable_str: str):
        return variable_str.upper()

    @classmethod
    def lower(cls, variable_str: str):
        return variable_str.lower()


class UnionSettings(object):

    def __init__(self, *args):
        # update this dict from global settings (but only for ALL_CAPS settings)
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))

        # store the settings module in case someone later cares
        self.SETTINGS_MODULE = None
        self.EXTRA_SETTING_MODULE = args  # type:list

        self.SETTINGS_MODULE = os.environ.get(ENVIRONMENT_VARIABLE)
        if not self.SETTINGS_MODULE:
            raise ImproperlyConfigured(
                "You must either define the environment variable %s "
                "or call settings.configure() before accessing settings."
                % (ENVIRONMENT_VARIABLE,))

        [self.setting_init(i) for i in self.EXTRA_SETTING_MODULE]
        if self.SETTINGS_MODULE:
            self.setting_init(self.SETTINGS_MODULE)

    def setting_init(self, settings_module_str):
        mod = importlib.import_module(settings_module_str)
        tuple_settings = (
            "INSTALLED_APPS",
            "TEMPLATE_DIRS",
            "LOCALE_PATHS",
        )
        self._explicit_settings = set()
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)

                if (setting in tuple_settings and
                        not isinstance(setting_value, (list, tuple))):
                    raise ImproperlyConfigured("The %s setting must be a list or a tuple. " % setting)
                setattr(self, setting, setting_value)
                self._explicit_settings.add(setting)

    def is_overridden(self, setting):
        return setting in self._explicit_settings

    def __repr__(self):
        return '<%(cls)s "%(settings_module)s">' % {
            'cls': self.__class__.__name__,
            'settings_module': self.SETTINGS_MODULE,
        }

    def __setattr__(self, key, value):
        self.__dict__[key] = value
        super().__setattr__(key, value)

    def __getattr__(self, item):
        return getattr(self, item)


class MapClass(object):
    name = None

    @classmethod
    def get_class_map(cls: type, path_list: List[str]) -> dict:
        """
        可以在 path_list 中获取该类的所有子类
        :param path_list:确保里面的所有的字符串都能通过 importlib.import_module(str) 导包
        :return:{sub_cls.name:sub_cls}
        """
        class_map = {}
        class_map_value_list = []
        path_list = set(path_list)
        for path in path_list:
            path_obj = importlib.import_module(path)
            cls_list = [getattr(path_obj, i) for i in path_obj.__dict__]
            cls_list = [i for i in cls_list if
                        isinstance(i, type) and i != cls and issubclass(i, cls)]
            class_map_value_list += cls_list
        class_map_value_list = list(set(class_map_value_list))
        for i in class_map_value_list:
            if class_map.get(i.name):
                raise Exception("错误！ {}类 和 {}类 指向的 name 一致".format(i.__name__, class_map[i.name].__name__))
            class_map[i.name] = i
        return class_map
