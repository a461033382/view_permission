# -*- coding: utf-8 -*-
# @Time    : 2021/6/18 15:00
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : permissions.py
# @Software: PyCharm

import json
from view_permission.permissions.symbol import Symbol, Equal, Lt, Gt, Lte, Gte, In, Allow, SymbolMap
from typing import TypeVar, List, Dict
import pandas as pd
from datetime import date, datetime


class ParamJsonObj(object):
    def __init__(self, param_name: str, value, symbol=None):
        self.param_name = param_name
        self.value = value
        self.symbol = symbol or Equal
        self._check()

    @classmethod
    def from_k_v(cls, k: str, v: object):
        if not isinstance(k, str):
            raise TypeError("错误:k必须为字符串:{}".format(k))
        k_list = k.split("__")
        if len(k_list) > 2:
            raise ValueError("错误：变量名中有过多的'__':{}".format(k))
        if len(k_list) == 1:
            param_name = k_list[0]
            return ParamJsonObj(param_name=param_name, value=v)
        else:
            param_name, symbol = k_list
            if symbol not in SymbolMap.keys():
                raise ValueError("错误：未知的运算符号：{}".format(k))
            return ParamJsonObj(param_name=param_name, value=v, symbol=SymbolMap[symbol])

    def _check(self):
        if self.symbol is None:
            return True
        if not issubclass(self.symbol, Symbol):
            raise TypeError("错误：无效的运算符号(symbol)")
        if not isinstance(self.param_name, str):
            raise TypeError("错误：变量名必须是字符串(str)")
        if "__" in self.param_name:
            raise KeyError("错误：变量不允许出现 __ ：{}".format(self.param_name))
        if self.param_name.endswith("_") or self.param_name.startswith("_"):
            raise KeyError("错误：变量的开头和结尾不允许出现 _ ：{}".format(self.param_name))
        if not self.symbol._check(val=self.value):
            raise TypeError(
                "错误：限制参数不合法！ 限制参数：{} ,类型：{}，限制值：{}".format(self.param_name, self.symbol.__name__, self.value))
        return True

    def __str__(self):
        if self.symbol:
            k = "{}__{}".format(self.param_name, self.symbol.json_str)
        else:
            k = self.param_name
        return json.dumps({k: self.value})

    def __call__(self, *args, **kwargs):
        if self.symbol:
            k = "{}__{}".format(self.param_name, self.symbol.json_str)
        else:
            k = self.param_name
        return {k: self.value}


class LimitJsonObj(object):
    def __init__(self):
        self.param_list = []  # type:List[ParamJsonObj]

    def __call__(self, **kwargs):
        for param in self.param_list:
            if not param.symbol.verify(param_name=param.param_name, val=param.value, tar=kwargs):
                return False
        return True

    def get_param_name_list(self):
        return list(set([i.param_name for i in self.param_list]))

    def add(self, param_name: str, value: object, symbol=None):
        symbol = symbol or Equal
        if not issubclass(symbol, Symbol):
            raise TypeError("错误的运算符号")
        self.param_list.append(ParamJsonObj(param_name, value, symbol))

    @classmethod
    def from_json_str(cls, json_str):
        param_list = LimitJsonObj.json_loads(json_str=json_str)
        obj = LimitJsonObj()
        obj.param_list = param_list
        return obj

    def to_df(self):
        d1 = [
            "param_name",
            "symbol",
            "value"
        ]
        df = pd.DataFrame(columns=d1)
        for i in range(len(self.param_list)):
            df.loc[i] = [self.param_list[i].param_name, self.param_list[i].symbol.chinese_name,
                         str(self.param_list[i].value)]
        return df

    @staticmethod
    def json_loads(json_str):
        try:
            json_obj = json.loads(json_str)  # type:dict
        except json.decoder.JSONDecodeError as e:
            json_obj = json.loads("{}")
        param_list = [ParamJsonObj.from_k_v(k, v) for k, v in json_obj.items()]
        return param_list

    def json_dumps(self):
        param_dict = [i() for i in self.param_list]
        res = {}
        for i in param_dict:
            for j in i.keys():
                res[j] = i[j]
        return json.dumps(res)

    def __str__(self):
        return self.json_dumps()


class ReqInfoJsonObj(object):

    def __init__(self, **kwargs):
        self.req_info = dict(**kwargs)

    @classmethod
    def from_json_str(cls, json_str):
        try:
            json_obj = json.loads(json_str)  # type:dict
        except json.decoder.JSONDecodeError as e:
            json_obj = json.loads("{}")
        return ReqInfoJsonObj(**json_obj)

    def to_json_str(self):
        return json.dumps(self.req_info)

    def add(self, param_name, value):
        self.req_info[param_name] = value

    def to_df(self):
        d1 = ["param_name", "value"
              ]
        df = pd.DataFrame(columns=d1)
        for num, key in zip(range(len(self.req_info)), self.req_info.keys()):
            df.loc[num] = [key, self.req_info[key]]
        return df


class Permission(object):
    def get_all_view(self):
        pass

    def add(self):
        pass


if __name__ == '__main__':
    a = LimitJsonObj()
    a.add("time_type", "yesterday")
    a.add("page", 1, Lte)
    a.add("page_size", 10, Lte)
    a.add("start_date", False, Allow)
    a.add("end_date", False, Allow)
    a.add("sort_key", "sort_key")
    a.add("platform", "all")
    print(a)
