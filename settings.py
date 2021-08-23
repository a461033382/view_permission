import os

#####################
#   BASE_SETTING    #
#####################

VIEW_PERMISSION_APP_NAME = "vp"
VIEW_PERMISSION_APP_PATH = os.path.dirname(__file__)

#####################
#   MODEL_SETTING   #
#####################

GROUP_MODEL_NAME = "vp_groups"
PERMISSION_MODEL_NAME = "vp_permissions"
VIEW_MODEL_NAME = "vp_views"

#####################
#   MODEL_SETTING   #
#####################

BASE_EXCLUDE_APP_NAMES = [
    "admin",
    "api-docs"
]

EXCLUDE_APP_NAMES = []
