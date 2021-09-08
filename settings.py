import os

#####################
#   BASE_SETTING    #
#####################

VIEW_PERMISSION_APP_FULL_NAME = 'view_permission'
VIEW_PERMISSION_APP_NAME = "vp"
VIEW_PERMISSION_APP_PATH = os.path.dirname(__file__)

#####################
#   MODEL_SETTING   #
#####################

GROUP_MODEL_NAME = "vp_groups"
PERMISSION_MODEL_NAME = "vp_permissions"
VIEW_MODEL_NAME = "vp_views"
USER_TO_GROUP_FIELD_NAME = "view_group_id"  # 用户表中的权限外键名

#####################
#   APP_SETTING     #
#####################

BASE_EXCLUDE_APP_NAMES = [
    "admin",
    "api-docs"
]

EXCLUDE_APP_NAMES = []

#####################
#   VIP_SETTING     #
#####################

BASE_VIP_DIR = [
    'view_permission.base.vip'
]

VIP_DIR = []

# 默认VIP名
NON_LOGIN_NAME = "NON_LOGIN"
BASE_VIP_NAME = "BASE_NAME"
SUPER_USER_NAME = "SUPER_USER"

#####################
#   VIEW_SETTING    #
#####################

HTTP_METHOD_NAMES = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
