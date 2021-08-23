# -*- coding: utf-8 -*-
# @Time    : 2021/7/22 16:26
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : symbol.py
# @Software: PyCharm

from datetime import date, datetime
import datetime as _datetime
from view_permission.base.utils import Utils


class Symbol(object):
    json_str = ""
    chinese_name = ""

    def __init__(self):
        pass

    @classmethod
    def _check(cls, val: object):
        return True

    @classmethod
    def _verify(cls, val, tar=None):
        return True

    @classmethod
    def type_tran(cls, t: type = None, s=None):
        return s

    @classmethod
    def get_param_name(cls, s: str):
        if not cls.json_str:
            return s
        if s.endswith("__{}".format(cls.json_str)):
            return s.replace("__{}".format(cls.json_str), "")
        else:
            raise KeyError("错误：无法获取到param_name。变量名：{}，运算符：{}".format(s, cls.json_str))

    @classmethod
    def verify(cls, param_name: str, val, tar: dict):
        if not tar or not isinstance(tar, dict):
            pass
        return cls._verify(val, tar.get(param_name))


class ThanSymbol(Symbol):
    """ 用于比较大小的运算符 """
    json_str = ""

    @classmethod
    def type_tran(cls, t: type = None, s=None):
        if s is None:
            return None

        if not t:
            if isinstance(s, str):
                s = Utils.is_int(s)
            if isinstance(s, str):
                s = Utils.is_date(s)
            return s

        if t == date:
            return date.fromisoformat(s)
        if t == datetime:
            return datetime.fromisoformat(s)
        if t == int:
            return int(s)
        else:
            return s

    @classmethod
    def _check(cls, val):
        if not val:
            return False

        if not isinstance(val, (int, float, date, datetime)):
            return False
        return True

    @classmethod
    def verify(cls, param_name: str, val, tar: dict):
        if not tar or not isinstance(tar, dict):
            pass
        return cls._verify(val, cls.type_tran(type(val), tar.get(param_name)))


class Equal(Symbol):
    json_str = "equal"
    chinese_name = "等于"

    @classmethod
    def _check(cls, val: object):
        return True

    @classmethod
    def _verify(cls, val, tar=None):
        if not cls._check(val):
            return False
        if not tar:
            return True
        return str(val) == tar


class Lt(ThanSymbol):
    """ 小于 """
    json_str = "lt"
    chinese_name = "小于"

    @classmethod
    def _verify(cls, val, tar=None):
        if not cls._check(val):
            return False
        if tar is None:
            return True
        if type(val) != type(tar):
            return False
        return tar < val


class Lte(ThanSymbol):
    """ 小于等于 """
    json_str = "lte"
    chinese_name = "小于等于"

    @classmethod
    def _verify(cls, val, tar=None):
        if not cls._check(val):
            return False
        if tar is None:
            return True
        if type(val) != type(tar):
            return False
        return tar <= val


class Gte(ThanSymbol):
    """ 大于等于 """
    json_str = "gte"
    chinese_name = "大于等于"

    @classmethod
    def _verify(cls, val, tar=None):
        if not cls._check(val):
            return False
        if tar is None:
            return True
        if type(val) != type(tar):
            return False
        return tar >= val


class Gt(ThanSymbol):
    """ 大于 """
    json_str = "gt"
    chinese_name = "大于"

    @classmethod
    def _verify(cls, val, tar=None):
        if not cls._check(val):
            return False
        if tar is None:
            return True
        if type(val) != type(tar):
            return False
        return tar > val


class In(ThanSymbol):
    """ 仅在列表中选取 """
    json_str = "in"
    chinese_name = "列表选取"

    @classmethod
    def _verify(cls, val, tar=None):
        """ 验证传入的参数是否满足该权限限制 """
        if not cls._check(val):
            return False
        if tar is None:
            return True
        if tar not in val:
            return False
        return True


class Allow(Symbol):
    """ 是否允许传入 """
    json_str = "allow"
    chinese_name = "是否允许"

    @classmethod
    def _check(cls, val: object):
        """ 验证传入的限制参数是否符合要求 """
        if val is None:
            return False
        if not isinstance(val, bool):
            return False
        return True

    @classmethod
    def type_tran(cls, t: type = None, s=None):
        if not t:
            if s:
                return True
            else:
                return False

    @classmethod
    def _verify(cls, val, tar=None):
        """ 验证传入的参数是否满足该权限限制 """
        if not cls._check(val):
            return False
        if not val and tar is not None:
            return False
        return True


SymbolMap = {
    "equal": Equal,
    "lt": Lt,
    "gt": Gt,
    "lte": Lte,
    "gte": Gte,
    "in": In,
    "allow": Allow
}
