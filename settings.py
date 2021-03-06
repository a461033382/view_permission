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
USER_VIEW_COUNT_MODEL_NAME = "vp_user_call_count"
VIEW_MODEL_NAME = "vp_views"
USER_TO_GROUP_FIELD_NAME = "view_group"  # 用户表中的权限外键名
VIEW_FIELD_NAME = "view"
USER_FIELD_NAME = "user"

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

#####################
#    CALL_LIMIT     #
#####################

CALL_LIMIT_CRON = "0 0 * * *"  # 默认为一天0点刷新一次
NEXT_RESET_TIME_CACHE_KEY = "next_reset_time"
