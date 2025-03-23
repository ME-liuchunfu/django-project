from rest_framework import serializers

from system.models import SysConfig, SysDept, SysDictData, SysDictType, SysMenu, SysNotice, \
    SysPost, SysRole, SysRoleDept, SysRoleMenu, SysUser, SysUserPost, SysUserRole


class SysConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysConfig
        fields = '__all__'


class SysDeptSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysDept
        fields = "__all__"


class SysDictDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysDictData
        fields = "__all__"


class SysDictTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysDictType
        fields = "__all__"


class SysMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysMenu
        fields = "__all__"


class SysNoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysNotice
        fields = "__all__"

class SysPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysPost
        fields = "__all__"


class SysRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysRole
        fields = "__all__"


class SysRoleDeptSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysRoleDept
        fields = "__all__"


class SysRoleMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysRoleMenu
        fields = "__all__"


class SysUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysUser
        exclude = ("password",)


class SysUserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysUserPost
        fields = "__all__"


class SysUserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysUserRole
        fields = "__all__"


