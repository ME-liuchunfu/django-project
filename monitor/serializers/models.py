from rest_framework import serializers

from monitor.models import SysLogininfor, SysOperLog


class SysLogininforSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysLogininfor
        fields = "__all__"



class SysOperLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysOperLog
        fields = "__all__"
