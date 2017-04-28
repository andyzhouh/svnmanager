# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-28 07:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='cmdb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('AssetType', models.CharField(max_length=100, verbose_name='\u8d44\u4ea7\u7c7b\u578b')),
                ('AssetSn', models.CharField(max_length=50, verbose_name='\u8d44\u4ea7\u7f16\u53f7')),
                ('ServerName', models.CharField(max_length=100, verbose_name='\u8d44\u4ea7\u540d')),
                ('IP', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP\u5730\u5740')),
                ('MAC', models.CharField(blank=True, max_length=50, null=True, verbose_name='MAC\u5730\u5740')),
                ('ServerType', models.CharField(max_length=50, verbose_name='\u8d44\u4ea7\u578b\u53f7')),
                ('ServerSN', models.CharField(max_length=50, verbose_name='\u8d44\u4ea7SN')),
                ('Disk', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u786c\u76d8')),
                ('DiskSN', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u786c\u76d8\u5e8f\u5217\u53f7')),
                ('RaidInfo', models.CharField(blank=True, max_length=100, null=True, verbose_name='Raid\u4fe1\u606f')),
                ('Mem', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u5185\u5b58')),
                ('CPU', models.CharField(blank=True, max_length=100, null=True)),
                ('iDracIP', models.GenericIPAddressField(blank=True, null=True, verbose_name='\u7ba1\u7406IP')),
                ('Memo', models.CharField(blank=True, max_length=200, null=True, verbose_name='\u5907\u6ce8')),
            ],
        ),
        migrations.CreateModel(
            name='hostgroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_groupname', models.CharField(max_length=30)),
                ('create_date', models.CharField(max_length=30)),
                ('create_user', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='hosts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_name', models.CharField(max_length=30)),
                ('host_user', models.CharField(max_length=30)),
                ('host_pass', models.CharField(blank=True, max_length=50, null=True)),
                ('host_w_ip', models.GenericIPAddressField()),
                ('host_w_port', models.PositiveIntegerField()),
                ('host_n_ip', models.GenericIPAddressField()),
                ('host_n_port', models.PositiveIntegerField()),
                ('host_root_pwd', models.CharField(blank=True, max_length=50, null=True)),
                ('script_dir', models.CharField(max_length=100)),
                ('host_description', models.TextField(blank=True)),
                ('create_user', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='online',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shost', models.GenericIPAddressField(verbose_name='\u9884\u53d1\u5e03\u673a')),
                ('sdir', models.CharField(max_length=100)),
                ('sexcludedir', models.CharField(blank=True, max_length=100, null=True)),
                ('ddir', models.CharField(max_length=100)),
                ('dhost', models.ManyToManyField(to='app01.hosts')),
            ],
        ),
        migrations.CreateModel(
            name='online_permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_info', models.CharField(blank=True, max_length=100, null=True)),
                ('web_users', models.CharField(max_length=100)),
                ('src_dir', models.TextField()),
            ],
            options={
                'verbose_name': '\u4e0a\u7ebf\u4ee3\u7801\u6743\u9650\u8868',
                'verbose_name_plural': '\u4e0a\u7ebf\u4ee3\u7801\u6743\u9650\u8868',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='\u6743\u9650\u540d\u79f0')),
                ('url', models.CharField(max_length=255, verbose_name='URL\u540d\u79f0')),
                ('per_method', models.SmallIntegerField(choices=[(1, 'GET'), (2, 'POST')], default=1, verbose_name='\u8bf7\u6c42\u65b9\u6cd5')),
                ('argument_list', models.CharField(blank=True, help_text='\u591a\u4e2a\u53c2\u6570\u4e4b\u95f4\u7528\u82f1\u6587\u534a\u89d2\u9017\u53f7\u9694\u5f00', max_length=255, null=True, verbose_name='\u53c2\u6570\u5217\u8868')),
                ('describe', models.CharField(max_length=255, verbose_name='\u63cf\u8ff0')),
            ],
            options={
                'verbose_name': '\u9875\u9762\u6743\u9650\u8868',
                'verbose_name_plural': '\u9875\u9762\u6743\u9650\u8868',
                'permissions': (('views_svns_list', '\u67e5\u770bsvn\u7248\u672c\u5e93\u4fe1\u606f\u8868'), ('views_onlinecode_info', '\u67e5\u770b\u63a8\u9001\u4ee3\u7801\u8be6\u7ec6\u4fe1\u606f\u8868'), ('views_assets_info', '\u67e5\u770b\u8d44\u4ea7\u8be6\u7ec6\u4fe1\u606f\u8868')),
            },
        ),
        migrations.CreateModel(
            name='scriptgroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('script_groupname', models.CharField(max_length=30)),
                ('create_date', models.CharField(max_length=30)),
                ('create_user', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='scripts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('script_name', models.CharField(max_length=30)),
                ('script_file', models.FileField(upload_to='aop/script/')),
                ('script_date', models.CharField(max_length=50)),
                ('script_description', models.TextField(blank=True)),
                ('create_user', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='svn_permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_info', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'SVN\u6743\u9650\u8868',
                'verbose_name_plural': 'SVN\u6743\u9650\u8868',
            },
        ),
        migrations.CreateModel(
            name='svns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('svn_name', models.CharField(max_length=20)),
                ('svn_user', models.CharField(max_length=30)),
                ('svn_pass', models.CharField(max_length=30)),
                ('svn_local', models.CharField(max_length=100)),
                ('svn_path', models.CharField(max_length=100)),
                ('create_user', models.CharField(max_length=10)),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.hosts')),
            ],
        ),
        migrations.CreateModel(
            name='tasks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=50)),
                ('task_date', models.CharField(max_length=50)),
                ('task_status', models.CharField(max_length=10)),
                ('task_create_user', models.CharField(max_length=30)),
                ('host_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.hostgroup')),
                ('script_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.scriptgroup')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='\u59d3\u540d')),
                ('iphone', models.CharField(max_length=11, verbose_name='\u624b\u673a')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='svn_permission',
            name='svn_projects',
            field=models.ManyToManyField(to='app01.svns'),
        ),
        migrations.AddField(
            model_name='svn_permission',
            name='web_users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='scriptgroup',
            name='script',
            field=models.ManyToManyField(to='app01.scripts'),
        ),
        migrations.AddField(
            model_name='hostgroup',
            name='host',
            field=models.ManyToManyField(to='app01.hosts'),
        ),
    ]
