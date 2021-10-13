from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.manager import Manager
from view_permission.conf import settings

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.apps import get_user_model


# Create your models here.

class ViewModel(models.Model):
    request_method = (
        ("1", "GET"),
        ("2", "POST"),
        ("3", "PUT"),
        ("4", "PATCH"),
        ("5", "DELETE"),
        ("6", "HEAD"),
        ("7", "OPTIONS"),
        ("8", "TRACE"),
    )

    request_method_dict = {
        "1": "GET",
        "2": "POST",
        "3": "PUT",
        "4": "PATCH",
        "5": "DELETE",
        "6": "HEAD",
        "7": "OPTIONS",
        "8": "TRACE",
    }
    request_method_dict_T = {
        "GET": "1",
        "POST": "2",
        "PUT": "3",
        "PATCH": "4",
        "DELETE": "5",
        "HEAD": "6",
        "OPTIONS": "7",
        "TRACE": "8",
    }
    view = models.CharField(max_length=50, verbose_name='视图名')
    name = models.CharField(max_length=50, verbose_name='权限名')
    url = models.CharField(max_length=50, verbose_name='URL')
    method = models.CharField(choices=request_method, verbose_name='请求方式', max_length=50)
    comment = models.TextField(default="")
    param_json = models.TextField(default="")
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    objects = Manager()

    class Meta:
        verbose_name = "视图信息"
        verbose_name_plural = "视图信息"
        db_table = settings.VIEW_MODEL_NAME

    def __str__(self):
        return self.name


class PermissionModel(models.Model):
    name = models.CharField(max_length=100, verbose_name='权限名')
    view = models.ForeignKey(to=ViewModel, on_delete=models.DO_NOTHING, to_field="id")
    param_json = models.TextField(verbose_name="参数限制", default="{}", null=True, blank=True)
    req_info = models.TextField(verbose_name="传入参数", default="{}", null=True, blank=True)
    need_login = models.BooleanField(default=False, verbose_name="是否需要登录")
    is_allow = models.BooleanField(default=True, verbose_name="是否允许请求")
    call_limit = models.IntegerField(default=-1, verbose_name="请求次数上限")

    objects = Manager()

    class Meta:
        verbose_name = "权限信息"
        verbose_name_plural = "权限信息"
        db_table = settings.PERMISSION_MODEL_NAME

    def __str__(self):
        return self.name


class UserGroup(models.Model):
    name = models.CharField(_('name'), max_length=150, unique=True)
    view_permissions = models.ManyToManyField(
        PermissionModel,
        verbose_name='视图权限',
        blank=True,
    )
    contain = models.ForeignKey(to="self", null=True, on_delete=models.SET_NULL, verbose_name="完全包含的VIP组",
                                )

    objects = Manager()

    class Meta:
        verbose_name = "权限组"
        verbose_name_plural = "权限组"
        db_table = settings.GROUP_MODEL_NAME

    def get_contain_group_list(self, group_list=None):
        if not group_list:
            group_list = []
        if not self.contain:
            return group_list
        if self.contain in group_list:
            return group_list
        group_list.append(self.contain)
        return self.contain.get_contain_group_list(group_list)

    def __str__(self):
        return self.name


def get_base_vip():
    from view_permission.base.vip import BaseUser
    try:
        return BaseUser.get_model().id
    except Exception as e:
        return None


class VPUserBaseModel(AbstractUser):
    view_group = models.ForeignKey(
        to=UserGroup, verbose_name="视图权限组", on_delete=models.SET_DEFAULT,
        null=True, blank=True,
        db_column=settings.USER_TO_GROUP_FIELD_NAME,
        default=get_base_vip
    )

    class Meta:
        verbose_name = "VP用户表"
        verbose_name_plural = "VP用户表"
        abstract = True


class UserViewCountModel(models.Model):
    user_id = models.IntegerField()
    view = models.ForeignKey(to=ViewModel, on_delete=models.CASCADE)
    call_time = models.IntegerField(default=0)

    class Meta:
        verbose_name = "视图请求计数表"
        verbose_name_plural = "视图请求计数表"
        db_table = settings.USER_VIEW_COUNT_MODEL_NAME

    @classmethod
    def get_call_time(cls, user: VPUserBaseModel, view: ViewModel):
        instance = cls.objects.filter(user_id=user.id, view=view).first()  # type:UserViewCountModel
        if not instance:
            return 0
        return instance.call_time

    @classmethod
    def add_call_time(cls, user: VPUserBaseModel, view: ViewModel):
        instance = cls.objects.filter(user_id=user.id, view=view).first()  # type:UserViewCountModel
        if not instance:
            instance = cls.objects.create(user_id=user.id, view=view)
        instance.call_time += 1
        instance.save()


