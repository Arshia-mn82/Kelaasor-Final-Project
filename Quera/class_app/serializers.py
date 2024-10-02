from rest_framework import serializers
from .models import PublicClass, PrivateClass
import uuid


class PublicClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicClass
        fields = '__all__'

    def create(self, validated_data):
        unique_id = str(uuid.uuid4())
        validated_data['unique_id'] = unique_id
        return super().create(validated_data)


class PrivateClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateClass
        fields = '__all__'

    def create(self, validated_data):
        unique_id = str(uuid.uuid4())
        validated_data['unique_id'] = unique_id
        return super().create(validated_data)
