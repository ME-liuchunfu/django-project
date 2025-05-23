# Generated by Django 5.1.7 on 2025-03-23 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SysConfig',
            fields=[
                ('config_id', models.AutoField(db_comment='参数主键', primary_key=True, serialize=False)),
                ('config_name', models.CharField(blank=True, db_comment='参数名称', max_length=100, null=True)),
                ('config_key', models.CharField(blank=True, db_comment='参数键名', max_length=100, null=True)),
                ('config_value', models.CharField(blank=True, db_comment='参数键值', max_length=500, null=True)),
                ('config_type', models.CharField(blank=True, db_comment='系统内置（Y是 N否）', max_length=1, null=True)),
                ('create_by', models.CharField(blank=True, db_comment='创建者', max_length=64, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, db_comment='创建时间', null=True)),
                ('update_by', models.CharField(blank=True, db_comment='更新者', max_length=64, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, db_comment='更新时间', null=True)),
                ('remark', models.CharField(blank=True, db_comment='备注', max_length=500, null=True)),
            ],
            options={
                'db_table': 'sys_config',
                'db_table_comment': '参数配置表',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SysDept',
            fields=[
                ('dept_id', models.BigAutoField(db_comment='部门id', primary_key=True, serialize=False)),
                ('parent_id', models.BigIntegerField(blank=True, db_comment='父部门id', null=True)),
                ('ancestors', models.CharField(blank=True, db_comment='祖级列表', max_length=50, null=True)),
                ('dept_name', models.CharField(blank=True, db_comment='部门名称', max_length=30, null=True)),
                ('order_num', models.IntegerField(blank=True, db_comment='显示顺序', null=True)),
                ('leader', models.CharField(blank=True, db_comment='负责人', max_length=20, null=True)),
                ('phone', models.CharField(blank=True, db_comment='联系电话', max_length=11, null=True)),
                ('email', models.CharField(blank=True, db_comment='邮箱', max_length=50, null=True)),
                ('status', models.CharField(blank=True, db_comment='部门状态（0正常 1停用）', max_length=1, null=True)),
                ('del_flag', models.CharField(blank=True, db_comment='删除标志（0代表存在 2代表删除）', max_length=1, null=True)),
                ('create_by', models.CharField(blank=True, db_comment='创建者', max_length=64, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, db_comment='创建时间', null=True)),
                ('update_by', models.CharField(blank=True, db_comment='更新者', max_length=64, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, db_comment='更新时间', null=True)),
            ],
            options={
                'db_table': 'sys_dept',
                'db_table_comment': '部门表',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SysDictData',
            fields=[
                ('dict_code', models.BigAutoField(db_comment='字典编码', primary_key=True, serialize=False)),
                ('dict_sort', models.IntegerField(blank=True, db_comment='字典排序', null=True)),
                ('dict_label', models.CharField(blank=True, db_comment='字典标签', max_length=100, null=True)),
                ('dict_value', models.CharField(blank=True, db_comment='字典键值', max_length=100, null=True)),
                ('dict_type', models.CharField(blank=True, db_comment='字典类型', max_length=100, null=True)),
                ('css_class', models.CharField(blank=True, db_comment='样式属性（其他样式扩展）', max_length=100, null=True)),
                ('list_class', models.CharField(blank=True, db_comment='表格回显样式', max_length=100, null=True)),
                ('is_default', models.CharField(blank=True, db_comment='是否默认（Y是 N否）', max_length=1, null=True)),
                ('status', models.CharField(blank=True, db_comment='状态（0正常 1停用）', max_length=1, null=True)),
                ('create_by', models.CharField(blank=True, db_comment='创建者', max_length=64, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, db_comment='创建时间', null=True)),
                ('update_by', models.CharField(blank=True, db_comment='更新者', max_length=64, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, db_comment='更新时间', null=True)),
                ('remark', models.CharField(blank=True, db_comment='备注', max_length=500, null=True)),
            ],
            options={
                'db_table': 'sys_dict_data',
                'db_table_comment': '字典数据表',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SysDictType',
            fields=[
                ('dict_id', models.BigAutoField(db_comment='字典主键', primary_key=True, serialize=False)),
                ('dict_name', models.CharField(blank=True, db_comment='字典名称', max_length=100, null=True)),
                ('dict_type', models.CharField(blank=True, db_comment='字典类型', max_length=100, null=True, unique=True)),
                ('status', models.CharField(blank=True, db_comment='状态（0正常 1停用）', max_length=1, null=True)),
                ('create_by', models.CharField(blank=True, db_comment='创建者', max_length=64, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, db_comment='创建时间', null=True)),
                ('update_by', models.CharField(blank=True, db_comment='更新者', max_length=64, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, db_comment='更新时间', null=True)),
                ('remark', models.CharField(blank=True, db_comment='备注', max_length=500, null=True)),
            ],
            options={
                'db_table': 'sys_dict_type',
                'db_table_comment': '字典类型表',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SysMenu',
            fields=[
                ('menu_id', models.BigAutoField(db_comment='菜单ID', primary_key=True, serialize=False)),
                ('menu_name', models.CharField(db_comment='菜单名称', max_length=50)),
                ('parent_id', models.BigIntegerField(blank=True, db_comment='父菜单ID', null=True)),
                ('order_num', models.IntegerField(blank=True, db_comment='显示顺序', null=True)),
                ('path', models.CharField(blank=True, db_comment='路由地址', max_length=200, null=True)),
                ('component', models.CharField(blank=True, db_comment='组件路径', max_length=255, null=True)),
                ('query', models.CharField(blank=True, db_comment='路由参数', max_length=255, null=True)),
                ('route_name', models.CharField(blank=True, db_comment='路由名称', max_length=50, null=True)),
                ('is_frame', models.CharField(blank=True, db_comment='是否为外链（0是 1否）', max_length=10, null=True)),
                ('is_cache', models.CharField(blank=True, db_comment='是否缓存（0缓存 1不缓存）', max_length=10, null=True)),
                ('menu_type', models.CharField(blank=True, db_comment='菜单类型（M目录 C菜单 F按钮）', max_length=1, null=True)),
                ('visible', models.CharField(blank=True, db_comment='菜单状态（0显示 1隐藏）', max_length=1, null=True)),
                ('status', models.CharField(blank=True, db_comment='菜单状态（0正常 1停用）', max_length=1, null=True)),
                ('perms', models.CharField(blank=True, db_comment='权限标识', max_length=100, null=True)),
                ('icon', models.CharField(blank=True, db_comment='菜单图标', max_length=100, null=True)),
                ('create_by', models.CharField(blank=True, db_comment='创建者', max_length=64, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, db_comment='创建时间', null=True)),
                ('update_by', models.CharField(blank=True, db_comment='更新者', max_length=64, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, db_comment='更新时间', null=True)),
                ('remark', models.CharField(blank=True, db_comment='备注', max_length=500, null=True)),
            ],
            options={
                'db_table': 'sys_menu',
                'db_table_comment': '菜单权限表',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SysNotice',
            fields=[
                ('notice_id', models.AutoField(db_comment='公告ID', primary_key=True, serialize=False)),
                ('notice_title', models.CharField(db_comment='公告标题', max_length=50)),
                ('notice_type', models.CharField(db_comment='公告类型（1通知 2公告）', max_length=1)),
                ('notice_content', models.TextField(blank=True, db_comment='公告内容', null=True)),
                ('status', models.CharField(blank=True, db_comment='公告状态（0正常 1关闭）', max_length=1, null=True)),
                ('create_by', models.CharField(blank=True, db_comment='创建者', max_length=64, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, db_comment='创建时间', null=True)),
                ('update_by', models.CharField(blank=True, db_comment='更新者', max_length=64, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, db_comment='更新时间', null=True)),
                ('remark', models.CharField(blank=True, db_comment='备注', max_length=255, null=True)),
            ],
            options={
                'db_table': 'sys_notice',
                'db_table_comment': '通知公告表',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SysPost',
            fields=[
                ('post_id', models.BigAutoField(db_comment='岗位ID', primary_key=True, serialize=False)),
                ('post_code', models.CharField(db_comment='岗位编码', max_length=64)),
                ('post_name', models.CharField(db_comment='岗位名称', max_length=50)),
                ('post_sort', models.IntegerField(db_comment='显示顺序')),
                ('status', models.CharField(db_comment='状态（0正常 1停用）', max_length=1)),
                ('create_by', models.CharField(blank=True, db_comment='创建者', max_length=64, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, db_comment='创建时间', null=True)),
                ('update_by', models.CharField(blank=True, db_comment='更新者', max_length=64, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, db_comment='更新时间', null=True)),
                ('remark', models.CharField(blank=True, db_comment='备注', max_length=500, null=True)),
            ],
            options={
                'db_table': 'sys_post',
                'db_table_comment': '岗位信息表',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SysRole',
            fields=[
                ('role_id', models.BigAutoField(db_comment='角色ID', primary_key=True, serialize=False)),
                ('role_name', models.CharField(db_comment='角色名称', max_length=30)),
                ('role_key', models.CharField(db_comment='角色权限字符串', max_length=100)),
                ('role_sort', models.IntegerField(db_comment='显示顺序')),
                ('data_scope', models.CharField(blank=True, db_comment='数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）', max_length=1, null=True)),
                ('menu_check_strictly', models.IntegerField(blank=True, db_comment='菜单树选择项是否关联显示', null=True)),
                ('dept_check_strictly', models.IntegerField(blank=True, db_comment='部门树选择项是否关联显示', null=True)),
                ('status', models.CharField(db_comment='角色状态（0正常 1停用）', max_length=1)),
                ('del_flag', models.CharField(blank=True, db_comment='删除标志（0代表存在 2代表删除）', max_length=1, null=True)),
                ('create_by', models.CharField(blank=True, db_comment='创建者', max_length=64, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, db_comment='创建时间', null=True)),
                ('update_by', models.CharField(blank=True, db_comment='更新者', max_length=64, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, db_comment='更新时间', null=True)),
                ('remark', models.CharField(blank=True, db_comment='备注', max_length=500, null=True)),
            ],
            options={
                'db_table': 'sys_role',
                'db_table_comment': '角色信息表',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SysRoleDept',
            fields=[
                ('role_id', models.BigIntegerField(db_comment='角色ID', primary_key=True, serialize=False)),
                ('dept_id', models.BigIntegerField(db_comment='部门ID')),
            ],
            options={
                'db_table': 'sys_role_dept',
                'db_table_comment': '角色和部门关联表',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SysRoleMenu',
            fields=[
                ('role_id', models.BigIntegerField(db_comment='角色ID', primary_key=True, serialize=False)),
                ('menu_id', models.BigIntegerField(db_comment='菜单ID')),
            ],
            options={
                'db_table': 'sys_role_menu',
                'db_table_comment': '角色和菜单关联表',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SysUser',
            fields=[
                ('user_id', models.BigAutoField(db_comment='用户ID', primary_key=True, serialize=False)),
                ('dept_id', models.BigIntegerField(blank=True, db_comment='部门ID', null=True)),
                ('username', models.CharField(db_column='user_name', db_comment='用户账号', max_length=30)),
                ('nick_name', models.CharField(db_comment='用户昵称', max_length=30)),
                ('user_type', models.CharField(blank=True, db_comment='用户类型（00系统用户）', max_length=2, null=True)),
                ('email', models.CharField(blank=True, db_comment='用户邮箱', max_length=50, null=True)),
                ('phonenumber', models.CharField(blank=True, db_comment='手机号码', max_length=11, null=True)),
                ('sex', models.CharField(blank=True, db_comment='用户性别（0男 1女 2未知）', max_length=1, null=True)),
                ('avatar', models.CharField(blank=True, db_comment='头像地址', max_length=100, null=True)),
                ('password', models.CharField(blank=True, db_comment='密码', max_length=100, null=True)),
                ('status', models.CharField(blank=True, db_comment='帐号状态（0正常 1停用）', max_length=1, null=True)),
                ('del_flag', models.CharField(blank=True, db_comment='删除标志（0代表存在 2代表删除）', max_length=1, null=True)),
                ('login_ip', models.CharField(blank=True, db_comment='最后登录IP', max_length=128, null=True)),
                ('login_date', models.DateTimeField(blank=True, db_comment='最后登录时间', null=True)),
                ('create_by', models.CharField(blank=True, db_comment='创建者', max_length=64, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, db_comment='创建时间', null=True)),
                ('update_by', models.CharField(blank=True, db_comment='更新者', max_length=64, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, db_comment='更新时间', null=True)),
                ('remark', models.CharField(blank=True, db_comment='备注', max_length=500, null=True)),
            ],
            options={
                'db_table': 'sys_user',
                'db_table_comment': '用户信息表',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SysUserPost',
            fields=[
                ('user_id', models.BigIntegerField(db_comment='用户ID', primary_key=True, serialize=False)),
                ('post_id', models.BigIntegerField(db_comment='岗位ID')),
            ],
            options={
                'db_table': 'sys_user_post',
                'db_table_comment': '用户与岗位关联表',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SysUserRole',
            fields=[
                ('user_id', models.BigIntegerField(db_comment='用户ID', primary_key=True, serialize=False)),
                ('role_id', models.BigIntegerField(db_comment='角色ID')),
            ],
            options={
                'db_table': 'sys_user_role',
                'db_table_comment': '用户和角色关联表',
                'managed': False,
            },
        ),
    ]
