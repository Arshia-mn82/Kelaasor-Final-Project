from rest_framework import serializers
from .models import Task, SingleTask, GroupTask
from class_app.models import PublicClass, PrivateClass
from account_app.models import Account


class TaskSerializer(serializers.ModelSerializer):
    public_class_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )
    private_class_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=True
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "description",
            "first_deadline",
            "second_deadline",
            "submit_limit",
            "score_bar",
            "answer_type",
            "question_bank",
            "public_class_ids",
            "private_class_ids",
        ]

    def validate_public_class_ids(self, public_class_ids):
        user = self.context["request"].user
        try:
            user_account = Account.objects.get(user=user)
            for class_id in public_class_ids:
                try:
                    public_class = PublicClass.objects.get(id=class_id)
                    if (
                        user_account not in public_class.teachers.all()
                        and user_account not in public_class.mentors.all()
                    ):
                        raise serializers.ValidationError(
                            f"You are not authorized to create tasks for public class {public_class.title}"
                        )
                except PublicClass.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Public class with id {class_id} does not exist."
                    )
        except Account.DoesNotExist:
            raise serializers.ValidationError("User account does not exist.")
        return public_class_ids

    def validate_private_class_ids(self, private_class_ids):
        user = self.context["request"].user
        try:
            user_account = Account.objects.get(user=user)
            for class_id in private_class_ids:
                try:
                    private_class = PrivateClass.objects.get(id=class_id)
                    if (
                        user_account not in private_class.teachers.all()
                        and user_account not in private_class.mentors.all()
                    ):
                        raise serializers.ValidationError(
                            f"You are not authorized to create tasks for private class {private_class.title}"
                        )
                except PrivateClass.DoesNotExist:
                    raise serializers.ValidationError(
                        f"Private class with id {class_id} does not exist."
                    )
        except Account.DoesNotExist:
            raise serializers.ValidationError("User account does not exist.")
        return private_class_ids

    def create(self, validated_data):
        public_class_ids = validated_data.pop("public_class_ids")
        private_class_ids = validated_data.pop("private_class_ids")
        task = super().create(validated_data)
        for class_id in public_class_ids:
            try:
                public_class = PublicClass.objects.get(id=class_id)
                public_class.tasks.add(task)
            except PublicClass.DoesNotExist:
                continue
        for class_id in private_class_ids:
            try:
                private_class = PrivateClass.objects.get(id=class_id)
                private_class.tasks.add(task)
            except PrivateClass.DoesNotExist:
                continue
        return task


class SingleTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SingleTask
        fields = ["id", "user", "task", "score", "score_bar", "result"]


class GroupTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupTask
        fields = ["id", "users", "group_name", "task", "score", "score_bar", "result"]
