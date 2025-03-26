from django.db import models

from manage import settings

# Create your models here.

table_managed = settings.DJANGO_APP_DATABASES_TABLES_MANAGE
if not table_managed:
    table_managed = table_managed

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
