from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Task, SingleTask, GroupTask
from .serializers import TaskSerializer, SingleTaskSerializer, GroupTaskSerializer
from account_app.models import Account
from class_app.models import PublicClass, PrivateClass


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        public_class_ids = self.request.data.get("public_class_ids", [])
        private_class_ids = self.request.data.get("private_class_ids", [])

        try:
            user_account = Account.objects.get(user=self.request.user)
        except Account.DoesNotExist:
            return Response(
                {"detail": "Account not found."}, status=status.HTTP_404_NOT_FOUND
            )

        public_classes = PublicClass.objects.filter(id__in=public_class_ids)
        private_classes = PrivateClass.objects.filter(id__in=private_class_ids)

        is_teacher_in_public = public_classes.filter(teachers=user_account).exists()
        is_teacher_in_private = private_classes.filter(teachers=user_account).exists()
        is_mentor_in_public = public_classes.filter(mentors=user_account).exists()
        is_mentor_in_private = private_classes.filter(mentors=user_account).exists()

        if not (
            is_teacher_in_public
            or is_teacher_in_private
            or is_mentor_in_public
            or is_mentor_in_private
        ):
            return Response(
                {"detail": "You are not authorized to add tasks to these classes."},
                status=status.HTTP_403_FORBIDDEN,
            )

        task = serializer.save()

        for cls in public_classes:
            cls.tasks.add(task)

        for cls in private_classes:
            cls.tasks.add(task)

        response_data = {
            "id": task.id,
            "name": task.name,
            "tasks": [task.name],
        }

        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        task = self.get_object()
        public_class_ids = self.request.data.get("public_class_ids", [])
        private_class_ids = self.request.data.get("private_class_ids", [])

        try:
            user_account = Account.objects.get(user=self.request.user)
        except Account.DoesNotExist:
            return Response(
                {"detail": "Account not found."}, status=status.HTTP_404_NOT_FOUND
            )

        public_classes = PublicClass.objects.filter(id__in=public_class_ids)
        private_classes = PrivateClass.objects.filter(id__in=private_class_ids)

        is_teacher_in_public = public_classes.filter(teachers=user_account).exists()
        is_teacher_in_private = private_classes.filter(teachers=user_account).exists()
        is_mentor_in_public = public_classes.filter(mentors=user_account).exists()
        is_mentor_in_private = private_classes.filter(mentors=user_account).exists()

        if not (
            is_teacher_in_public
            or is_teacher_in_private
            or is_mentor_in_public
            or is_mentor_in_private
        ):
            return Response(
                {"detail": "You are not authorized to update this task."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer.save()

        response_data = {
            "id": task.id,
            "name": task.name,
            "tasks": [task.name],
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        public_classes = instance.publicclass_set.all()
        private_classes = instance.privateclass_set.all()

        try:
            user_account = Account.objects.get(user=self.request.user)
        except Account.DoesNotExist:
            return Response(
                {"detail": "Account not found."}, status=status.HTTP_404_NOT_FOUND
            )

        is_teacher_in_public = any(
            cls.teachers.filter(id=user_account.id).exists() for cls in public_classes
        )
        is_teacher_in_private = any(
            cls.teachers.filter(id=user_account.id).exists() for cls in private_classes
        )
        is_mentor_in_public = any(
            cls.mentors.filter(id=user_account.id).exists() for cls in public_classes
        )
        is_mentor_in_private = any(
            cls.mentors.filter(id=user_account.id).exists() for cls in private_classes
        )

        if not (
            is_teacher_in_public
            or is_teacher_in_private
            or is_mentor_in_public
            or is_mentor_in_private
        ):
            return Response(
                {"detail": "You are not authorized to delete this task."},
                status=status.HTTP_403_FORBIDDEN,
            )

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssignSingleTaskView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SingleTaskSerializer

    def perform_create(self, serializer):
        public_class_ids = self.request.data.get("public_class_ids", [])
        private_class_ids = self.request.data.get("private_class_ids", [])
        user_account = Account.objects.get(user=self.request.user)
        print("It is here")

        for public_class_id in public_class_ids:
            public_class_obj = PublicClass.objects.get(id=public_class_id)
            if (
                user_account not in public_class_obj.teachers.all()
                and user_account not in public_class_obj.mentors.all()
            ):
                raise PermissionError("Permission denied for public class.")

        for private_class_id in private_class_ids:
            private_class_obj = PrivateClass.objects.get(id=private_class_id)
            if (
                user_account not in private_class_obj.teachers.all()
                and user_account not in private_class_obj.mentors.all()
            ):
                raise PermissionError("Permission denied for private class.")

        serializer.save(user=user_account)


class AssignGroupTaskView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupTaskSerializer

    def perform_create(self, serializer):
        public_class_ids = self.request.data.get("public_class_ids", [])
        private_class_ids = self.request.data.get("private_class_ids", [])
        user_account = Account.objects.get(user=self.request.user)

        for public_class_id in public_class_ids:
            public_class_obj = PublicClass.objects.get(id=public_class_id)
            if (
                user_account not in public_class_obj.teachers.all()
                and user_account not in public_class_obj.mentors.all()
            ):
                raise PermissionError("Permission denied for public class.")

        for private_class_id in private_class_ids:
            private_class_obj = PrivateClass.objects.get(id=private_class_id)
            if (
                user_account not in private_class_obj.teachers.all()
                and user_account not in private_class_obj.mentors.all()
            ):
                raise PermissionError("Permission denied for private class.")

        serializer.save()


class UpdateSingleTaskView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SingleTaskSerializer
    queryset = SingleTask.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        public_class_ids = request.data.get("public_class_ids", [])
        private_class_ids = request.data.get("private_class_ids", [])
        user_account = Account.objects.get(user=request.user)

        for public_class_id in public_class_ids:
            public_class_obj = PublicClass.objects.get(id=public_class_id)
            if (
                user_account not in public_class_obj.teachers.all()
                and user_account not in public_class_obj.mentors.all()
            ):
                return Response(
                    {"detail": "Permission denied for public class."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        for private_class_id in private_class_ids:
            private_class_obj = PrivateClass.objects.get(id=private_class_id)
            if (
                user_account not in private_class_obj.teachers.all()
                and user_account not in private_class_obj.mentors.all()
            ):
                return Response(
                    {"detail": "Permission denied for private class."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        return super().update(request, *args, **kwargs)


class UpdateGroupTaskView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GroupTaskSerializer
    queryset = GroupTask.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user_account = Account.objects.get(user=request.user)
        public_class_ids = request.data.get("public_class_ids", [])
        private_class_ids = request.data.get("private_class_ids", [])

        for public_class_id in public_class_ids:
            public_class_obj = PublicClass.objects.get(id=public_class_id)
            if (
                user_account not in public_class_obj.teachers.all()
                and user_account not in public_class_obj.mentors.all()
            ):
                return Response(
                    {"detail": "Permission denied for public class."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        for private_class_id in private_class_ids:
            private_class_obj = PrivateClass.objects.get(id=private_class_id)
            if (
                user_account not in private_class_obj.teachers.all()
                and user_account not in private_class_obj.mentors.all()
            ):
                return Response(
                    {"detail": "Permission denied for private class."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        return super().update(request, *args, **kwargs)


class DeleteSingleTaskView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SingleTask.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user_account = Account.objects.get(user=request.user)

        public_class_id = instance.public_class_id
        private_class_id = instance.private_class_id

        if public_class_id:
            public_class_obj = PublicClass.objects.get(id=public_class_id)
            if (
                user_account not in public_class_obj.teachers.all()
                and user_account not in public_class_obj.mentors.all()
            ):
                return Response(
                    {"detail": "Permission denied for public class."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        if private_class_id:
            private_class_obj = PrivateClass.objects.get(id=private_class_id)
            if (
                user_account not in private_class_obj.teachers.all()
                and user_account not in private_class_obj.mentors.all()
            ):
                return Response(
                    {"detail": "Permission denied for private class."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        return super().destroy(request, *args, **kwargs)


class DeleteGroupTaskView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = GroupTask.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user_account = Account.objects.get(user=request.user)

        public_class_id = instance.public_class_id
        private_class_id = instance.private_class_id

        if public_class_id:
            public_class_obj = PublicClass.objects.get(id=public_class_id)
            if (
                user_account not in public_class_obj.teachers.all()
                and user_account not in public_class_obj.mentors.all()
            ):
                return Response(
                    {"detail": "Permission denied for public class."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        if private_class_id:
            private_class_obj = PrivateClass.objects.get(id=private_class_id)
            if (
                user_account not in private_class_obj.teachers.all()
                and user_account not in private_class_obj.mentors.all()
            ):
                return Response(
                    {"detail": "Permission denied for private class."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        return super().destroy(request, *args, **kwargs)


class RetrieveSingleTaskView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SingleTask.objects.all()
    serializer_class = SingleTaskSerializer


class RetrieveGroupTaskView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = GroupTask.objects.all()
    serializer_class = GroupTaskSerializer
