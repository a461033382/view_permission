# Generated by Django 2.2.3 on 2021-08-31 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view_permission', '0002_auto_20210819_1731'),
    ]

    operations = [
        migrations.AddField(
            model_name='permissionmodel',
            name='is_allow',
            field=models.BooleanField(default=True, verbose_name='是否允许请求'),
        ),
    ]
