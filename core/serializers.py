from rest_framework import serializers
from . import utils

from .models import Customer, StageChangeEvent, Stage

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
        fields = ['id', 'description', 'from_stage_id', 'to_stage_id', 'customer', 'created_at', 'updated_at']
