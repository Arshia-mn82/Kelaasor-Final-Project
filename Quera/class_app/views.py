from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PublicClass, PrivateClass
from .serializers import PublicClassSerializer, PrivateClassSerializer


class PublicClassViewSet(viewsets.ModelViewSet):
    queryset = PublicClass.objects.all()
    serializer_class = PublicClassSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        class_instance = self.get_object()
        if request.user in class_instance.teachers.all():
            serializer = self.get_serializer(class_instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response({"detail": "You do not have permission to modify this class."}, status=403)


class PrivateClassViewSet(viewsets.ModelViewSet):
    queryset = PrivateClass.objects.all()
    serializer_class = PrivateClassSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        class_instance = self.get_object()
        if request.user in class_instance.teachers.all():
            serializer = self.get_serializer(class_instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response({"detail": "You do not have permission to modify this class."}, status=403)

    def create(self, request, *args, **kwargs):
        data = request.data
        if data['signup_type'] == PrivateClass.PASSWORD:
            password = data.get('password')
            # handle password logic
        else:
            # handle invitation link logic
            pass
        return super().create(request, *args, **kwargs)
