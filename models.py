from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.manager import Manager
from view_permission.conf import settings


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
    param_json = models.TextField(verbose_name="参数限制")
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

    objects = Manager()

    class Meta:
        verbose_name = "权限组"
        verbose_name_plural = "权限组"
        db_table = settings.GROUP_MODEL_NAME

    def __str__(self):
        return self.name
