# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-05-02 02:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0014_auto_20170428_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='svn_permission',
            name='permission_info',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.RemoveField(
            model_name='svn_permission',
            name='svn_projects',
        ),
        migrations.AddField(
            model_name='svn_permission',
            name='svn_projects',
            field=models.TextField(default='111'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='svn_permission',
            name='web_users',
        ),
        migrations.AddField(
            model_name='svn_permission',
            name='web_users',
            field=models.CharField(default='ddd', max_length=100),
            preserve_default=False,
        ),
    ]
