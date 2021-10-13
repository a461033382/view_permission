# -*- coding: utf-8 -*-
# @Time    : 2021/7/27 10:42
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : vpinit.py
# @Software: PyCharm
import streamlit as st
import os
import sys
import django


@st.cache(allow_output_mutation=True)
def start_django(django_project_path, settings_path_str):
    sys.path.insert(0, django_project_path)
    manage_path = os.path.join(django_project_path, "manage.py")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", manage_path)
    django.setup()


start_django(*sys.argv[1:3])

from view_permission.permissions.permission import LimitJsonObj, ReqInfoJsonObj
from view_permission.permissions.symbol import SymbolMap
from view_permission.models import PermissionModel, UserGroup, ViewModel


class BaseStreamLit(object):

    def main_back(self):
        pass

    def sidebar(self):
        pass

    def run(self):
        self.sidebar()
        self.main_back()


class Test(BaseStreamLit):

    def __init__(self):
        self.view = None
        self.group = None
        self.permission = None
        self.permission_obj = None  # type:PermissionModel

    def sidebar(self):
        all_group = UserGroup.objects.all()
        self.group = st.sidebar.selectbox("组", ["-"] + [i.name for i in all_group])
        all_view = ViewModel.objects.all()
        self.view = st.sidebar.selectbox("视图", ["-"] + [i.name for i in all_view])
        filter_map = {}
        if self.group != "-":
            filter_map["usergroup__name"] = self.group
        if self.view != "-":
            filter_map["view__name"] = self.view
        all_permission = PermissionModel.objects.filter(**filter_map).all()
        self.permission = st.sidebar.selectbox("权限", ["-"] + [i.name for i in all_permission])

    def main_back(self):
        if not self.permission or self.permission == "-":
            return None
        self.permission_obj = PermissionModel.objects.filter(name=self.permission).first()  # type:PermissionModel
        if not self.permission_obj:
            st.error("未找到该权限")
        self.device()
        self.main_back_show()

    def device(self):

        need_login = st.sidebar.checkbox(label="是否需要登录状态",
                                         value=self.permission_obj.need_login,
                                         )
        is_allow = st.sidebar.checkbox(label="是否允许请求",
                                       value=self.permission_obj.is_allow)

        self.permission_obj.need_login = need_login
        self.permission_obj.is_allow = is_allow
        self.permission_obj.save()

        limit_json = self.permission_obj.param_json
        limit_obj = LimitJsonObj.from_json_str(limit_json)
        limit_df = limit_obj.to_df()
        index_list = range(len(limit_obj.param_list))

        req_info_json = self.permission_obj.req_info
        req_info_obj = ReqInfoJsonObj.from_json_str(req_info_json)
        req_info_df = req_info_obj.to_df()
        req_info_index_list = range(len(req_info_obj.req_info))

        st.sidebar.write("限制变量")

        with st.sidebar.form("add_limit_param"):
            st.write("添加变量")
            # Every form must have a submit button.
            param_name = st.text_input(label="变量名")
            value = st.text_input(label="限制值")
            symbol = st.selectbox(label="运算符号", options=[i.json_str for i in SymbolMap.values()],
                                  format_func=lambda x: SymbolMap[x].chinese_name,
                                  )
            add_button = st.form_submit_button("添加")
            if add_button:
                self.add_limit_param(param_name=param_name, value=value, symbol=symbol)
                st.experimental_rerun()

        with st.sidebar.form("delete_limit_param"):
            st.write("删除变量")
            delete_select_box = st.selectbox("请选择需要删除的变量", index_list,
                                             format_func=lambda x: "{} {} {}".format(
                                                 *limit_df.loc[x].to_dict().values())
                                             )
            delete_button_box = st.form_submit_button("删除")
            if delete_button_box:
                self.delete_limit_param(delete_select_box)
                st.experimental_rerun()

        st.sidebar.write("传输变量")

        with st.sidebar.form("add_req_info"):
            st.write("添加变量")
            param_name = st.text_input(label="变量名")
            value = st.text_input(label="值")
            add_button = st.form_submit_button("添加")
            if add_button:
                self.add_req_info(param_name=param_name, value=value)
                st.experimental_rerun()

        with st.sidebar.form("delete_req_info"):
            st.write("删除变量")
            delete_select_box = st.selectbox("请选择需要删除的变量", req_info_index_list,
                                             format_func=lambda x: "{} = {}".format(
                                                 *req_info_df.loc[x].to_dict().values())
                                             )
            delete_button_box = st.form_submit_button("删除")
            if delete_button_box:
                self.delete_req_info(delete_select_box)
                st.experimental_rerun()

    def main_back_show(self):
        limit_json = self.permission_obj.param_json
        limit_obj = LimitJsonObj.from_json_str(limit_json)
        limit_df = limit_obj.to_df()
        st.table(limit_df)
        req_info = self.permission_obj.req_info or "{}"
        req_info_obj = ReqInfoJsonObj.from_json_str(req_info)
        st.table(req_info_obj.to_df())

    def delete_limit_param(self, param_index):
        param_json = self.permission_obj.param_json
        limit_obj = LimitJsonObj.from_json_str(param_json)
        limit_obj.param_list.pop(param_index)
        self.permission_obj.param_json = limit_obj.__str__()
        self.permission_obj.save()

    def add_limit_param(self, param_name, value, symbol):
        limit_obj = LimitJsonObj.from_json_str(self.permission_obj.param_json)
        symbol = SymbolMap[symbol]
        limit_obj.add(param_name, symbol.type_tran(s=value), symbol)
        self.permission_obj.param_json = limit_obj.__str__()
        self.permission_obj.save()

    def add_req_info(self, param_name, value):
        req_info = ReqInfoJsonObj.from_json_str(self.permission_obj.req_info)
        req_info.add(param_name, value)
        self.permission_obj.req_info = req_info.to_json_str()
        self.permission_obj.save()

    def delete_req_info(self, param_index):
        req_info_json = self.permission_obj.req_info
        req_info_obj = ReqInfoJsonObj.from_json_str(req_info_json)
        req_info_obj.req_info.pop(list(req_info_obj.req_info.keys())[param_index])
        self.permission_obj.req_info = req_info_obj.to_json_str()
        self.permission_obj.save()

    def change_bool(self, param, b):
        setattr(self.permission_obj, param, b)
        self.permission_obj.save()


if __name__ == '__main__':
    Test().run()
