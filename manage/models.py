# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class GenTable(models.Model):
    table_id = models.BigAutoField(primary_key=True, db_comment='编号')
    table_name = models.CharField(max_length=200, blank=True, null=True, db_comment='表名称')
    table_comment = models.CharField(max_length=500, blank=True, null=True, db_comment='表描述')
    sub_table_name = models.CharField(max_length=64, blank=True, null=True, db_comment='关联子表的表名')
    sub_table_fk_name = models.CharField(max_length=64, blank=True, null=True, db_comment='子表关联的外键名')
    class_name = models.CharField(max_length=100, blank=True, null=True, db_comment='实体类名称')
    tpl_category = models.CharField(max_length=200, blank=True, null=True, db_comment='使用的模板（crud单表操作 tree树表操作）')
    tpl_web_type = models.CharField(max_length=30, blank=True, null=True, db_comment='前端模板类型（element-ui模版 element-plus模版）')
    package_name = models.CharField(max_length=100, blank=True, null=True, db_comment='生成包路径')
    module_name = models.CharField(max_length=30, blank=True, null=True, db_comment='生成模块名')
    business_name = models.CharField(max_length=30, blank=True, null=True, db_comment='生成业务名')
    function_name = models.CharField(max_length=50, blank=True, null=True, db_comment='生成功能名')
    function_author = models.CharField(max_length=50, blank=True, null=True, db_comment='生成功能作者')
    gen_type = models.CharField(max_length=1, blank=True, null=True, db_comment='生成代码方式（0zip压缩包 1自定义路径）')
    gen_path = models.CharField(max_length=200, blank=True, null=True, db_comment='生成路径（不填默认项目路径）')
    options = models.CharField(max_length=1000, blank=True, null=True, db_comment='其它生成选项')
    create_by = models.CharField(max_length=64, blank=True, null=True, db_comment='创建者')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='创建时间')
    update_by = models.CharField(max_length=64, blank=True, null=True, db_comment='更新者')
    update_time = models.DateTimeField(blank=True, null=True, db_comment='更新时间')
    remark = models.CharField(max_length=500, blank=True, null=True, db_comment='备注')

    class Meta:
        managed = False
        db_table = 'gen_table'
        db_table_comment = '代码生成业务表'


class GenTableColumn(models.Model):
    column_id = models.BigAutoField(primary_key=True, db_comment='编号')
    table_id = models.BigIntegerField(blank=True, null=True, db_comment='归属表编号')
    column_name = models.CharField(max_length=200, blank=True, null=True, db_comment='列名称')
    column_comment = models.CharField(max_length=500, blank=True, null=True, db_comment='列描述')
    column_type = models.CharField(max_length=100, blank=True, null=True, db_comment='列类型')
    java_type = models.CharField(max_length=500, blank=True, null=True, db_comment='JAVA类型')
    java_field = models.CharField(max_length=200, blank=True, null=True, db_comment='JAVA字段名')
    is_pk = models.CharField(max_length=1, blank=True, null=True, db_comment='是否主键（1是）')
    is_increment = models.CharField(max_length=1, blank=True, null=True, db_comment='是否自增（1是）')
    is_required = models.CharField(max_length=1, blank=True, null=True, db_comment='是否必填（1是）')
    is_insert = models.CharField(max_length=1, blank=True, null=True, db_comment='是否为插入字段（1是）')
    is_edit = models.CharField(max_length=1, blank=True, null=True, db_comment='是否编辑字段（1是）')
    is_list = models.CharField(max_length=1, blank=True, null=True, db_comment='是否列表字段（1是）')
    is_query = models.CharField(max_length=1, blank=True, null=True, db_comment='是否查询字段（1是）')
    query_type = models.CharField(max_length=200, blank=True, null=True, db_comment='查询方式（等于、不等于、大于、小于、范围）')
    html_type = models.CharField(max_length=200, blank=True, null=True, db_comment='显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件）')
    dict_type = models.CharField(max_length=200, blank=True, null=True, db_comment='字典类型')
    sort = models.IntegerField(blank=True, null=True, db_comment='排序')
    create_by = models.CharField(max_length=64, blank=True, null=True, db_comment='创建者')
    create_time = models.DateTimeField(blank=True, null=True, db_comment='创建时间')
    update_by = models.CharField(max_length=64, blank=True, null=True, db_comment='更新者')
    update_time = models.DateTimeField(blank=True, null=True, db_comment='更新时间')

    class Meta:
        managed = False
        db_table = 'gen_table_column'
        db_table_comment = '代码生成业务表字段'







