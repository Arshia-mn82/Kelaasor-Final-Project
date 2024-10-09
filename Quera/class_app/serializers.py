from rest_framework import serializers
from .models import PublicClass, PrivateClass
from account_app.models import *
from task_app.models import Task


class PublicClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicClass
        fields = ["title", "description"]
        extra_kwargs = {
            "title": {"required": True},
            "description": {"required": True},
        }


class PrivateClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateClass
        fields = ["title", "description", "signup_type", "password"]
        extra_kwargs = {
            "title": {"required": True},
            "description": {"required": True},
            "signup_type": {"required": True},
            "password": {
                "required": False
            },  # Password is optional, only required for password-protected classes
        }

    def validate(self, data):
        if data["signup_type"] == PrivateClass.PASSWORD and not data.get("password"):
            raise serializers.ValidationError(
                {"password": "Password is required for password-protected classes."}
            )
        return data


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "name" , "first_deadline"]


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "first_name", "last_name"]


class PublicClassDetailSerializer(serializers.ModelSerializer):
    teachers = AccountSerializer(many=True)
    students = AccountSerializer(many=True)
    mentors = AccountSerializer(many=True)
    tasks = TaskSerializer(many=True)

    class Meta:
        model = PublicClass
        fields = [
            "id",
            "title",
            "description",
            "capacity",
            "start_register_date",
            "end_register_date",
            "teachers",
            "students",
            "mentors",
            "tasks",
            "forum",
        ]


class PrivateClassDetailSerializer(serializers.ModelSerializer):
    teachers = AccountSerializer(many=True)
    students = AccountSerializer(many=True)
    mentors = AccountSerializer(many=True)
    tasks = TaskSerializer(many=True)

    class Meta:
        model = PrivateClass
        fields = [
            "id",
            "title",
            "description",
            "capacity",
            "signup_type",
            "password",
            "start_register_date",
            "end_register_date",
            "teachers",
            "students",
            "mentors",
            "tasks",
            "forum",
        ]
