from rest_framework import serializers

from generator.models import GenTable, GenTableColumn, VerTableInfo


class GenTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = GenTable
        fields = '__all__'


class VerTableInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerTableInfo
        fields = '__all__'


class GenTableColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenTableColumn
        fields = '__all__'