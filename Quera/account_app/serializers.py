from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account
from django.contrib.auth.hashers import make_password


class AccountSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Account
        fields = [
            "user",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):

        account = Account.objects.create(
            user=validated_data["user"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone_number=validated_data["phone_number"],
            email=validated_data["email"],
            password=make_password(validated_data["password"]),
        )

        return account


class AccountListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id',
            'first_name',
            'last_name',
            'phone_number',
            'email',
        ]
        
class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            'password'
        ]