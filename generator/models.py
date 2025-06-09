from manage import settings
from django.db import models
from django.utils import timezone

table_managed = settings.DJANGO_APP_DATABASES_TABLES_MANAGE
if not table_managed:
    table_managed = table_managed


class GenTable(models.Model):
    """代码生成业务表"""

    # 基础信息
    table_id = models.BigAutoField(primary_key=True, verbose_name='编号')
    table_name = models.CharField(max_length=200, default='', verbose_name='表名称')
    table_comment = models.CharField(max_length=500, default='', verbose_name='表描述')

    # 关联信息
    sub_table_name = models.CharField(max_length=64, null=True, blank=True, verbose_name='关联子表的表名')
    sub_table_fk_name = models.CharField(max_length=64, null=True, blank=True, verbose_name='子表关联的外键名')

    # 代码生成配置
    class_name = models.CharField(max_length=100, default='', verbose_name='实体类名称')
    TPL_CHOICES = (
        ('crud', 'crud单表操作'),
        ('tree', 'tree树表操作'),
    )
    tpl_category = models.CharField(max_length=200, default='crud', choices=TPL_CHOICES, verbose_name='使用的模板')

    WEB_TYPE_CHOICES = (
        ('element-ui', 'element-ui模版'),
        ('element-plus', 'element-plus模版'),
    )
    tpl_web_type = models.CharField(max_length=30, default='', choices=WEB_TYPE_CHOICES, blank=True,
                                    verbose_name='前端模板类型')

    package_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='生成包路径')
    module_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='生成模块名')
    business_name = models.CharField(max_length=30, null=True, blank=True, verbose_name='生成业务名')
    function_name = models.CharField(max_length=50, null=True, blank=True, verbose_name='生成功能名')
    function_author = models.CharField(max_length=50, null=True, blank=True, verbose_name='生成功能作者')

    GEN_TYPE_CHOICES = (
        ('0', 'zip压缩包'),
        ('1', '自定义路径'),
    )
    gen_type = models.CharField(max_length=1, default='0', choices=GEN_TYPE_CHOICES, verbose_name='生成代码方式')
    gen_path = models.CharField(max_length=200, default='/', verbose_name='生成路径')
    options = models.CharField(max_length=1000, null=True, blank=True, verbose_name='其它生成选项')

    # 审计信息
    create_by = models.CharField(max_length=64, default='', verbose_name='创建者')
    create_time = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    update_by = models.CharField(max_length=64, default='', verbose_name='更新者')
    update_time = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')
    remark = models.CharField(max_length=500, null=True, blank=True, verbose_name='备注')

    class Meta:
        managed = table_managed
        db_table = 'gen_table'
        verbose_name = '代码生成业务表'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        """自动更新时间戳"""
        if not self.create_time:
            self.create_time = timezone.now()
        self.update_time = timezone.now()
        super().save(*args, **kwargs)


class VerTableInfo(models.Model):
    table_name = models.CharField(primary_key=True, max_length=255)
    table_comment = models.TextField()
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False  # 不创建数据库表
        db_table = 'tables'  # 指向虚拟表


class GenTableColumn(models.Model):
    """代码生成业务表字段"""

    # 基础信息
    column_id = models.BigAutoField(primary_key=True, verbose_name='编号')
    table_id = models.BigIntegerField(null=True, blank=True, verbose_name='归属表编号')
    column_name = models.CharField(max_length=200, null=True, blank=True, verbose_name='列名称')
    column_comment = models.CharField(max_length=500, null=True, blank=True, verbose_name='列描述')
    column_type = models.CharField(max_length=100, null=True, blank=True, verbose_name='列类型')
    java_type = models.CharField(max_length=500, null=True, blank=True, verbose_name='JAVA类型')
    java_field = models.CharField(max_length=200, null=True, blank=True, verbose_name='JAVA字段名')

    # 字段属性（布尔类型用 CharField + 选择项）
    BOOLEAN_CHOICES = (
        ('1', '是'),
        ('0', '否'),
    )

    is_pk = models.CharField(max_length=1, null=True, blank=True, choices=BOOLEAN_CHOICES, verbose_name='是否主键')
    is_increment = models.CharField(max_length=1, null=True, blank=True, choices=BOOLEAN_CHOICES,
                                    verbose_name='是否自增')
    is_required = models.CharField(max_length=1, null=True, blank=True, choices=BOOLEAN_CHOICES,
                                   verbose_name='是否必填')
    is_insert = models.CharField(max_length=1, null=True, blank=True, choices=BOOLEAN_CHOICES,
                                 verbose_name='是否为插入字段')
    is_edit = models.CharField(max_length=1, null=True, blank=True, choices=BOOLEAN_CHOICES,
                               verbose_name='是否编辑字段')
    is_list = models.CharField(max_length=1, null=True, blank=True, choices=BOOLEAN_CHOICES,
                               verbose_name='是否列表字段')
    is_query = models.CharField(max_length=1, null=True, blank=True, choices=BOOLEAN_CHOICES,
                                verbose_name='是否查询字段')

    # 查询与显示设置
    QUERY_TYPE_CHOICES = (
        ('EQ', '等于'),
        ('NE', '不等于'),
        ('GT', '大于'),
        ('LT', '小于'),
        ('BT', '范围'),
        # 可根据需要添加更多
    )
    query_type = models.CharField(max_length=200, default='EQ', choices=QUERY_TYPE_CHOICES, verbose_name='查询方式')

    HTML_TYPE_CHOICES = (
        ('input', '文本框'),
        ('textarea', '文本域'),
        ('select', '下拉框'),
        ('checkbox', '复选框'),
        ('radio', '单选框'),
        ('date', '日期控件'),
        # 可根据需要添加更多
    )
    html_type = models.CharField(max_length=200, null=True, blank=True, choices=HTML_TYPE_CHOICES,
                                 verbose_name='显示类型')

    dict_type = models.CharField(max_length=200, default='', verbose_name='字典类型')
    sort = models.IntegerField(null=True, blank=True, verbose_name='排序')

    # 审计信息
    create_by = models.CharField(max_length=64, default='', verbose_name='创建者')
    create_time = models.DateTimeField(null=True, blank=True, verbose_name='创建时间')
    update_by = models.CharField(max_length=64, default='', verbose_name='更新者')
    update_time = models.DateTimeField(null=True, blank=True, verbose_name='更新时间')

    class Meta:
        managed = table_managed
        db_table = 'gen_table_column'
        verbose_name = '代码生成业务表字段'
        verbose_name_plural = verbose_name

    def save(self, *args, **kwargs):
        """自动更新时间戳"""
        if not self.create_time:
            self.create_time = timezone.now()
        self.update_time = timezone.now()
        super().save(*args, **kwargs)
