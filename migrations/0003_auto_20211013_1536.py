# Generated by Django 2.2.3 on 2021-10-13 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('view_permission', '0002_userviewcountmodel'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='userviewcountmodel',
            table='vp_user_call_count',
        ),
    ]
