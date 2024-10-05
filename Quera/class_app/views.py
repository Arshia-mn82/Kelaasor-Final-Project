from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import PublicClass, PrivateClass
from .serializers import *
from account_app.models import Account
import uuid
from django.shortcuts import get_object_or_404


def generate_unique_id():
    return str(uuid.uuid4())[:8]


def get_user_account(request):
    try:
        account = Account.objects.get(user=request.user)
        return account
    except Account.DoesNotExist:
        return None


def is_teacher_of_class(account, class_instance):
    return account in class_instance.teachers.all()


class CreatePublicClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PublicClassSerializer(data=request.data)

        if serializer.is_valid():
            new_public_class = PublicClass.objects.create(
                title=serializer.validated_data["title"],
                description=serializer.validated_data["description"],
                unique_id=generate_unique_id(),
            )

            account = get_user_account(request)
            if not account:
                return Response(
                    {"error": "Account for the user does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            new_public_class.teachers.add(account)
            new_public_class.save()

            return Response(
                {
                    "success": "Public Class Created",
                    "unique_id": new_public_class.unique_id,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePrivateClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PrivateClassSerializer(data=request.data)

        if serializer.is_valid():
            new_private_class = PrivateClass.objects.create(
                title=serializer.validated_data["title"],
                description=serializer.validated_data["description"],
                signup_type=serializer.validated_data["signup_type"],
                unique_id=generate_unique_id(),
            )

            if new_private_class.signup_type == PrivateClass.PASSWORD:
                new_private_class.password = serializer.validated_data["password"]

            account = get_user_account(request)
            if not account:
                return Response(
                    {"error": "Account for the user does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            new_private_class.teachers.add(account)
            new_private_class.save()

            return Response(
                {
                    "success": "Private Class Created",
                    "unique_id": new_private_class.unique_id,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PublicClassView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        public_classes = PublicClass.objects.all()
        serializer = PublicClassDetailSerializer(public_classes, many=True)
        return Response(serializer.data)


class PrivateClassView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        private_classes = PrivateClass.objects.all()
        serializer = PrivateClassDetailSerializer(private_classes, many=True)
        return Response(serializer.data)


class PublicClassDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        public_class = get_object_or_404(PublicClass, pk=pk)
        serializer = PublicClassDetailSerializer(public_class)
        return Response(serializer.data)


class PrivateClassDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        private_class = get_object_or_404(PrivateClass, pk=pk)
        serializer = PrivateClassSerializer(private_class)
        return Response(serializer.data)


class UpdatePublicClass(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        public_class = get_object_or_404(PublicClass, pk=pk)
        account = get_user_account(request)
        if not account:
            return Response(
                {"error": "Account for the user does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not is_teacher_of_class(account, public_class):
            return Response(
                {"error": "Only teachers of this class can update its details."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data
        public_class.title = data.get("title", public_class.title)
        public_class.description = data.get("description", public_class.description)
        public_class.capacity = data.get("capacity", public_class.capacity)
        public_class.start_register_date = data.get(
            "start_register_date", public_class.start_register_date
        )
        public_class.end_register_date = data.get(
            "end_register_date", public_class.end_register_date
        )

        public_class.save()
        serializer = PublicClassDetailSerializer(public_class)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdatePrivateClass(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        private_class = get_object_or_404(PrivateClass, pk=pk)
        account = get_user_account(request)
        if not account:
            return Response(
                {"error": "Account for the user does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not is_teacher_of_class(account, private_class):
            return Response(
                {"error": "Only teachers of this class can update its details."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data
        private_class.title = data.get("title", private_class.title)
        private_class.description = data.get("description", private_class.description)
        private_class.capacity = data.get("capacity", private_class.capacity)
        private_class.start_register_date = data.get(
            "start_register_date", private_class.start_register_date
        )
        private_class.end_register_date = data.get(
            "end_register_date", private_class.end_register_date
        )

        if "password" in data and private_class.signup_type == "P":
            private_class.password = data["password"]

        private_class.save()
        serializer = PrivateClassDetailSerializer(private_class)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddTeacherToPublicClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        public_class = get_object_or_404(PublicClass, pk=pk)
        account = get_user_account(request)
        if not account:
            return Response(
                {"error": "Account for the user does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not is_teacher_of_class(account, public_class):
            return Response(
                {"error": "Only teachers of this class can add other teachers."},
                status=status.HTTP_403_FORBIDDEN,
            )

        teacher_id = request.data.get("teacher_id")
        if not teacher_id:
            return Response(
                {"error": "Teacher ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            new_teacher = Account.objects.get(pk=teacher_id)
            public_class.teachers.add(new_teacher)
        except Account.DoesNotExist:
            return Response(
                {"error": "The teacher account does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        public_class.save()
        return Response(
            {"success": "Teacher added successfully."}, status=status.HTTP_200_OK
        )


class AddTeacherToPrivateClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        private_class = get_object_or_404(PrivateClass, pk=pk)
        account = get_user_account(request)
        if not account:
            return Response(
                {"error": "Account for the user does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not is_teacher_of_class(account, private_class):
            return Response(
                {"error": "Only teachers of this class can add other teachers."},
                status=status.HTTP_403_FORBIDDEN,
            )

        teacher_id = request.data.get("teacher_id")
        if not teacher_id:
            return Response(
                {"error": "Teacher ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            new_teacher = Account.objects.get(pk=teacher_id)
            private_class.teachers.add(new_teacher)
        except Account.DoesNotExist:
            return Response(
                {"error": "The teacher account does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        private_class.save()
        return Response(
            {"success": "Teacher added successfully."}, status=status.HTTP_200_OK
        )


class AddMentorToPublicClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        public_class = get_object_or_404(PublicClass, pk=pk)
        account = get_user_account(request)
        if not account:
            return Response(
                {"error": "Account for the user does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not is_teacher_of_class(account, public_class):
            return Response(
                {"error": "Only teachers of this class can add mentors."},
                status=status.HTTP_403_FORBIDDEN,
            )

        mentor_id = request.data.get("mentor_id")
        if not mentor_id:
            return Response(
                {"error": "Mentor ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            new_mentor = Account.objects.get(pk=mentor_id)
            public_class.mentors.add(new_mentor)
        except Account.DoesNotExist:
            return Response(
                {"error": "The mentor account does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        public_class.save()
        return Response(
            {"success": "Mentor added successfully."}, status=status.HTTP_200_OK
        )


class AddMentorToPrivateClass(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        private_class = get_object_or_404(PrivateClass, pk=pk)
        account = get_user_account(request)
        if not account:
            return Response(
                {"error": "Account for the user does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not is_teacher_of_class(account, private_class):
            return Response(
                {"error": "Only teachers of this class can add mentors."},
                status=status.HTTP_403_FORBIDDEN,
            )

        mentor_id = request.data.get("mentor_id")
        if not mentor_id:
            return Response(
                {"error": "Mentor ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            new_mentor = Account.objects.get(pk=mentor_id)
            private_class.mentors.add(new_mentor)
        except Account.DoesNotExist:
            return Response(
                {"error": "The mentor account does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        private_class.save()
        return Response(
            {"success": "Mentor added successfully."}, status=status.HTTP_200_OK
        )


class GetStudentsInPublicClass(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        public_class = get_object_or_404(PublicClass, pk=pk)
        account = get_user_account(request)
        if not account:
            return Response(
                {"error": "Account for the user does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not is_teacher_of_class(account, public_class):
            return Response(
                {"error": "Only teachers of this class can view students."},
                status=status.HTTP_403_FORBIDDEN,
            )

        students = (
            public_class.students.all()
        )  # Assuming you have a 'students' relation in PublicClass
        serializer = AccountSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetStudentsInPrivateClass(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        private_class = get_object_or_404(PrivateClass, pk=pk)
        account = get_user_account(request)
        if not account:
            return Response(
                {"error": "Account for the user does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not is_teacher_of_class(account, private_class):
            return Response(
                {"error": "Only teachers of this class can view students."},
                status=status.HTTP_403_FORBIDDEN,
            )

        students = private_class.students.all()
        serializer = AccountSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteStudentFromPublicClass(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, class_id, student_id):
        public_class = get_object_or_404(PublicClass, pk=class_id)
        account = get_user_account(request)
        if not account:
            return Response(
                {"error": "Account for the user does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not is_teacher_of_class(account, public_class):
            return Response(
                {"error": "Only teachers of this class can delete students."},
                status=status.HTTP_403_FORBIDDEN,
            )

        student = get_object_or_404(Account, id=student_id)
        public_class.students.remove(student)
        return Response(
            {"success": "Student removed successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class DeleteStudentFromPrivateClass(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk, student_id):
        private_class = get_object_or_404(PrivateClass, pk=pk)
        account = get_user_account(request)
        if not account:
            return Response(
                {"error": "Account for the user does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not is_teacher_of_class(account, private_class):
            return Response(
                {"error": "Only teachers of this class can delete students."},
                status=status.HTTP_403_FORBIDDEN,
            )

        student = get_object_or_404(Account, id=student_id)
        private_class.students.remove(student)
        return Response(
            {"success": "Student removed successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
