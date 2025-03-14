from django.conf import settings
from django.db import models

# Create your models here.

table_managed = settings.DJANGO_APP_DATABASES_TABLES_MANAGE
if not table_managed:
    table_managed = table_managed


class SysConfig(models.Model):
    config_id = models.AutoField(primary_key=True, db_comment='参数主键')
    config_name = models.CharField(max_length=100, blank=True, null=True, db_comment='参数名称')
    config_key = models.CharField(max_length=100, blank=True, null=True, db_comment='参数键名')
    config_value = models.CharField(max_length=500, blank=True, null=True, db_comment='参数键值')
    config_type = models.CharField(max_length=1, blank=True, null=True, db_comment='系统内置（Y是 N否）')
    create_by = models.CharField(max_length=64, blank=True, null=True, db_comment='创建者')
    create_time = models.DateTimeField(blank=True, auto_now_add=True, null=True, db_comment='创建时间')
    update_by = models.CharField(max_length=64, blank=True, null=True, db_comment='更新者')
    update_time = models.DateTimeField(blank=True, auto_now= True, null=True, db_comment='更新时间')
    remark = models.CharField(max_length=500, blank=True, null=True, db_comment='备注')

    class Meta:
        managed = table_managed
        db_table = 'sys_config'
        db_table_comment = '参数配置表'


class SysDept(models.Model):
    dept_id = models.BigAutoField(primary_key=True, db_comment='部门id')
    parent_id = models.BigIntegerField(blank=True, null=True, db_comment='父部门id')
    ancestors = models.CharField(max_length=50, blank=True, null=True, db_comment='祖级列表')
    dept_name = models.CharField(max_length=30, blank=True, null=True, db_comment='部门名称')
    order_num = models.IntegerField(blank=True, null=True, db_comment='显示顺序')
    leader = models.CharField(max_length=20, blank=True, null=True, db_comment='负责人')
    phone = models.CharField(max_length=11, blank=True, null=True, db_comment='联系电话')
    email = models.CharField(max_length=50, blank=True, null=True, db_comment='邮箱')
    status = models.CharField(max_length=1, blank=True, null=True, db_comment='部门状态（0正常 1停用）')
    del_flag = models.CharField(max_length=1, blank=True, null=True, db_comment='删除标志（0代表存在 2代表删除）')
    create_by = models.CharField(max_length=64, blank=True, null=True, db_comment='创建者')
    create_time = models.DateTimeField(blank=True, auto_now_add=True, null=True, db_comment='创建时间')
    update_by = models.CharField(max_length=64, blank=True, null=True, db_comment='更新者')
    update_time = models.DateTimeField(blank=True, auto_now= True, null=True, db_comment='更新时间')

    class Meta:
        managed = table_managed
        db_table = 'sys_dept'
        db_table_comment = '部门表'



class SysDictData(models.Model):
    dict_code = models.BigAutoField(primary_key=True, db_comment='字典编码')
    dict_sort = models.IntegerField(blank=True, null=True, db_comment='字典排序')
    dict_label = models.CharField(max_length=100, blank=True, null=True, db_comment='字典标签')
    dict_value = models.CharField(max_length=100, blank=True, null=True, db_comment='字典键值')
    dict_type = models.CharField(max_length=100, blank=True, null=True, db_comment='字典类型')
    css_class = models.CharField(max_length=100, blank=True, null=True, db_comment='样式属性（其他样式扩展）')
    list_class = models.CharField(max_length=100, blank=True, null=True, db_comment='表格回显样式')
    is_default = models.CharField(max_length=1, blank=True, null=True, db_comment='是否默认（Y是 N否）')
    status = models.CharField(max_length=1, blank=True, null=True, db_comment='状态（0正常 1停用）')
    create_by = models.CharField(max_length=64, blank=True, null=True, db_comment='创建者')
    create_time = models.DateTimeField(blank=True, auto_now_add=True, null=True, db_comment='创建时间')
    update_by = models.CharField(max_length=64, blank=True, null=True, db_comment='更新者')
    update_time = models.DateTimeField(blank=True, auto_now= True, null=True, db_comment='更新时间')
    remark = models.CharField(max_length=500, blank=True, null=True, db_comment='备注')

    class Meta:
        managed = table_managed
        db_table = 'sys_dict_data'
        db_table_comment = '字典数据表'


class SysDictType(models.Model):
    dict_id = models.BigAutoField(primary_key=True, db_comment='字典主键')
    dict_name = models.CharField(max_length=100, blank=True, null=True, db_comment='字典名称')
    dict_type = models.CharField(unique=True, max_length=100, blank=True, null=True, db_comment='字典类型')
    status = models.CharField(max_length=1, blank=True, null=True, db_comment='状态（0正常 1停用）')
    create_by = models.CharField(max_length=64, blank=True, null=True, db_comment='创建者')
    create_time = models.DateTimeField(blank=True, auto_now_add=True, null=True, db_comment='创建时间')
    update_by = models.CharField(max_length=64, blank=True, null=True, db_comment='更新者')
    update_time = models.DateTimeField(blank=True, auto_now= True, null=True, db_comment='更新时间')
    remark = models.CharField(max_length=500, blank=True, null=True, db_comment='备注')

    class Meta:
        managed = table_managed
        db_table = 'sys_dict_type'
        db_table_comment = '字典类型表'


class SysLogininfor(models.Model):
    info_id = models.BigAutoField(primary_key=True, db_comment='访问ID')
    user_name = models.CharField(max_length=50, blank=True, null=True, db_comment='用户账号')
    ipaddr = models.CharField(max_length=128, blank=True, null=True, db_comment='登录IP地址')
    login_location = models.CharField(max_length=255, blank=True, null=True, db_comment='登录地点')
    browser = models.CharField(max_length=50, blank=True, null=True, db_comment='浏览器类型')
    os = models.CharField(max_length=50, blank=True, null=True, db_comment='操作系统')
    status = models.CharField(max_length=1, blank=True, null=True, db_comment='登录状态（0成功 1失败）')
    msg = models.CharField(max_length=255, blank=True, null=True, db_comment='提示消息')
    login_time = models.DateTimeField(blank=True, null=True, db_comment='访问时间')

    class Meta:
        managed = table_managed
        db_table = 'sys_logininfor'
        db_table_comment = '系统访问记录'



class SysMenu(models.Model):
    menu_id = models.BigAutoField(primary_key=True, db_comment='菜单ID')
    menu_name = models.CharField(max_length=50, db_comment='菜单名称')
    parent_id = models.BigIntegerField(blank=True, null=True, db_comment='父菜单ID')
    order_num = models.IntegerField(blank=True, null=True, db_comment='显示顺序')
    path = models.CharField(max_length=200, blank=True, null=True, db_comment='路由地址')
    component = models.CharField(max_length=255, blank=True, null=True, db_comment='组件路径')
    query = models.CharField(max_length=255, blank=True, null=True, db_comment='路由参数')
    route_name = models.CharField(max_length=50, blank=True, null=True, db_comment='路由名称')
    is_frame = models.IntegerField(blank=True, null=True, db_comment='是否为外链（0是 1否）')
    is_cache = models.IntegerField(blank=True, null=True, db_comment='是否缓存（0缓存 1不缓存）')
    menu_type = models.CharField(max_length=1, blank=True, null=True, db_comment='菜单类型（M目录 C菜单 F按钮）')
    visible = models.CharField(max_length=1, blank=True, null=True, db_comment='菜单状态（0显示 1隐藏）')
    status = models.CharField(max_length=1, blank=True, null=True, db_comment='菜单状态（0正常 1停用）')
    perms = models.CharField(max_length=100, blank=True, null=True, db_comment='权限标识')
    icon = models.CharField(max_length=100, blank=True, null=True, db_comment='菜单图标')
    create_by = models.CharField(max_length=64, blank=True, null=True, db_comment='创建者')
    create_time = models.DateTimeField(blank=True, auto_now_add=True, null=True, db_comment='创建时间')
    update_by = models.CharField(max_length=64, blank=True, null=True, db_comment='更新者')
    update_time = models.DateTimeField(blank=True, auto_now= True, null=True, db_comment='更新时间')
    remark = models.CharField(max_length=500, blank=True, null=True, db_comment='备注')

    class Meta:
        managed = table_managed
        db_table = 'sys_menu'
        db_table_comment = '菜单权限表'


class SysNotice(models.Model):
    notice_id = models.AutoField(primary_key=True, db_comment='公告ID')
    notice_title = models.CharField(max_length=50, db_comment='公告标题')
    notice_type = models.CharField(max_length=1, db_comment='公告类型（1通知 2公告）')
    notice_content = models.TextField(blank=True, null=True, db_comment='公告内容')
    status = models.CharField(max_length=1, blank=True, null=True, db_comment='公告状态（0正常 1关闭）')
    create_by = models.CharField(max_length=64, blank=True, null=True, db_comment='创建者')
    create_time = models.DateTimeField(blank=True, auto_now_add=True, null=True, db_comment='创建时间')
    update_by = models.CharField(max_length=64, blank=True, null=True, db_comment='更新者')
    update_time = models.DateTimeField(blank=True, auto_now= True, null=True, db_comment='更新时间')
    remark = models.CharField(max_length=255, blank=True, null=True, db_comment='备注')

    class Meta:
        managed = table_managed
        db_table = 'sys_notice'
        db_table_comment = '通知公告表'


class SysOperLog(models.Model):
    oper_id = models.BigAutoField(primary_key=True, db_comment='日志主键')
    title = models.CharField(max_length=50, blank=True, null=True, db_comment='模块标题')
    business_type = models.IntegerField(blank=True, null=True, db_comment='业务类型（0其它 1新增 2修改 3删除）')
    method = models.CharField(max_length=200, blank=True, null=True, db_comment='方法名称')
    request_method = models.CharField(max_length=10, blank=True, null=True, db_comment='请求方式')
    operator_type = models.IntegerField(blank=True, null=True, db_comment='操作类别（0其它 1后台用户 2手机端用户）')
    oper_name = models.CharField(max_length=50, blank=True, null=True, db_comment='操作人员')
    dept_name = models.CharField(max_length=50, blank=True, null=True, db_comment='部门名称')
    oper_url = models.CharField(max_length=255, blank=True, null=True, db_comment='请求URL')
    oper_ip = models.CharField(max_length=128, blank=True, null=True, db_comment='主机地址')
    oper_location = models.CharField(max_length=255, blank=True, null=True, db_comment='操作地点')
    oper_param = models.CharField(max_length=2000, blank=True, null=True, db_comment='请求参数')
    json_result = models.CharField(max_length=2000, blank=True, null=True, db_comment='返回参数')
    status = models.IntegerField(blank=True, null=True, db_comment='操作状态（0正常 1异常）')
    error_msg = models.CharField(max_length=2000, blank=True, null=True, db_comment='错误消息')
    oper_time = models.DateTimeField(blank=True, null=True, db_comment='操作时间')
    cost_time = models.BigIntegerField(blank=True, null=True, db_comment='消耗时间')

    class Meta:
        managed = table_managed
        db_table = 'sys_oper_log'
        db_table_comment = '操作日志记录'


class SysPost(models.Model):
    post_id = models.BigAutoField(primary_key=True, db_comment='岗位ID')
    post_code = models.CharField(max_length=64, db_comment='岗位编码')
    post_name = models.CharField(max_length=50, db_comment='岗位名称')
    post_sort = models.IntegerField(db_comment='显示顺序')
    status = models.CharField(max_length=1, db_comment='状态（0正常 1停用）')
    create_by = models.CharField(max_length=64, blank=True, null=True, db_comment='创建者')
    create_time = models.DateTimeField(blank=True, auto_now_add=True, null=True, db_comment='创建时间')
    update_by = models.CharField(max_length=64, blank=True, null=True, db_comment='更新者')
    update_time = models.DateTimeField(blank=True, auto_now= True, null=True, db_comment='更新时间')
    remark = models.CharField(max_length=500, blank=True, null=True, db_comment='备注')

    class Meta:
        managed = table_managed
        db_table = 'sys_post'
        db_table_comment = '岗位信息表'


class SysRole(models.Model):
    role_id = models.BigAutoField(primary_key=True, db_comment='角色ID')
    role_name = models.CharField(max_length=30, db_comment='角色名称')
    role_key = models.CharField(max_length=100, db_comment='角色权限字符串')
    role_sort = models.IntegerField(db_comment='显示顺序')
    data_scope = models.CharField(max_length=1, blank=True, null=True, db_comment='数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）')
    menu_check_strictly = models.IntegerField(blank=True, null=True, db_comment='菜单树选择项是否关联显示')
    dept_check_strictly = models.IntegerField(blank=True, null=True, db_comment='部门树选择项是否关联显示')
    status = models.CharField(max_length=1, db_comment='角色状态（0正常 1停用）')
    del_flag = models.CharField(max_length=1, blank=True, null=True, db_comment='删除标志（0代表存在 2代表删除）')
    create_by = models.CharField(max_length=64, blank=True, null=True, db_comment='创建者')
    create_time = models.DateTimeField(blank=True, auto_now_add=True, null=True, db_comment='创建时间')
    update_by = models.CharField(max_length=64, blank=True, null=True, db_comment='更新者')
    update_time = models.DateTimeField(blank=True, auto_now= True, null=True, db_comment='更新时间')
    remark = models.CharField(max_length=500, blank=True, null=True, db_comment='备注')

    class Meta:
        managed = table_managed
        db_table = 'sys_role'
        db_table_comment = '角色信息表'


class SysRoleDept(models.Model):
    role_id = models.BigIntegerField(primary_key=True, db_comment='角色ID')  # The composite primary key (role_id, dept_id) found, that is not supported. The first column is selected.
    dept_id = models.BigIntegerField(db_comment='部门ID')

    class Meta:
        managed = table_managed
        db_table = 'sys_role_dept'
        unique_together = (('role_id', 'dept_id'),)
        db_table_comment = '角色和部门关联表'


class SysRoleMenu(models.Model):
    role_id = models.BigIntegerField(primary_key=True, db_comment='角色ID')  # The composite primary key (role_id, menu_id) found, that is not supported. The first column is selected.
    menu_id = models.BigIntegerField(db_comment='菜单ID')

    class Meta:
        managed = table_managed
        db_table = 'sys_role_menu'
        unique_together = (('role_id', 'menu_id'),)
        db_table_comment = '角色和菜单关联表'


class SysUser(models.Model):
    user_id = models.BigAutoField(primary_key=True, db_comment='用户ID')
    dept_id = models.BigIntegerField(blank=True, null=True, db_comment='部门ID')
    username = models.CharField(db_column="user_name", max_length=30, db_comment='用户账号')
    nick_name = models.CharField(max_length=30, db_comment='用户昵称')
    user_type = models.CharField(max_length=2, blank=True, null=True, db_comment='用户类型（00系统用户）')
    email = models.CharField(max_length=50, blank=True, null=True, db_comment='用户邮箱')
    phonenumber = models.CharField(max_length=11, blank=True, null=True, db_comment='手机号码')
    sex = models.CharField(max_length=1, blank=True, null=True, db_comment='用户性别（0男 1女 2未知）')
    avatar = models.CharField(max_length=100, blank=True, null=True, db_comment='头像地址')
    password = models.CharField(max_length=100, blank=True, null=True, db_comment='密码')
    status = models.CharField(max_length=1, blank=True, null=True, db_comment='帐号状态（0正常 1停用）')
    del_flag = models.CharField(max_length=1, blank=True, null=True, db_comment='删除标志（0代表存在 2代表删除）')
    login_ip = models.CharField(max_length=128, blank=True, null=True, db_comment='最后登录IP')
    login_date = models.DateTimeField(blank=True, null=True, db_comment='最后登录时间')
    create_by = models.CharField(max_length=64, blank=True, null=True, db_comment='创建者')
    create_time = models.DateTimeField(blank=True, auto_now_add=True, null=True, db_comment='创建时间')
    update_by = models.CharField(max_length=64, blank=True, null=True, db_comment='更新者')
    update_time = models.DateTimeField(blank=True, auto_now= True, null=True, db_comment='更新时间')
    remark = models.CharField(max_length=500, blank=True, null=True, db_comment='备注')

    class Meta:
        managed = table_managed
        db_table = 'sys_user'
        db_table_comment = '用户信息表'


class SysUserPost(models.Model):
    user_id = models.BigIntegerField(primary_key=True, db_comment='用户ID')  # The composite primary key (user_id, post_id) found, that is not supported. The first column is selected.
    post_id = models.BigIntegerField(db_comment='岗位ID')

    class Meta:
        managed = table_managed
        db_table = 'sys_user_post'
        unique_together = (('user_id', 'post_id'),)
        db_table_comment = '用户与岗位关联表'


class SysUserRole(models.Model):
    user_id = models.BigIntegerField(primary_key=True, db_comment='用户ID')  # The composite primary key (user_id, role_id) found, that is not supported. The first column is selected.
    role_id = models.BigIntegerField(db_comment='角色ID')

    class Meta:
        managed = table_managed
        db_table = 'sys_user_role'
        unique_together = (('user_id', 'role_id'),)
        db_table_comment = '用户和角色关联表'
