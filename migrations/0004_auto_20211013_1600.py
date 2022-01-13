# Generated by Django 2.2.3 on 2021-10-13 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('view_permission', '0003_auto_20211013_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permissionmodel',
            name='param_json',
            field=models.TextField(blank=True, default='{}', null=True, verbose_name='参数限制'),
        ),
        migrations.AlterField(
            model_name='permissionmodel',
            name='req_info',
            field=models.TextField(blank=True, default='{}', null=True, verbose_name='传入参数'),
        ),
        migrations.AlterField(
            model_name='userviewcountmodel',
            name='call_time',
            field=models.IntegerField(default=0),
        ),
    ]
