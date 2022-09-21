from rest_framework import serializers
from core.utils import group_stage_change_converter
from .models import Customer, StageChangeEvent, Stage, GroupStageChangeMapping


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'current_stage', 'created_at', 'updated_at']

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['id', 'name', 'slug', 'created_at', 'updated_at']

class StageChangeEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageChangeEvent
        fields = ['id', 'description', 'from_stage', 'to_stage', 'customer', 'created_at', 'updated_at']

class GroupStageChangeMappingSerializer(serializers.ModelSerializer):
    mapped_data = serializers.SerializerMethodField()

    def get_mapped_data(self, obj):
        return group_stage_change_converter(obj.mapping)

    class Meta:
        model = GroupStageChangeMapping
        fields = ['id', 'mapped_data', 'created_at', 'updated_at', 'name', 'mapping']
