from django.urls import path
from .views import *

urlpatterns = [
    path("create-public-class/", CreatePublicClass.as_view()),
    path("create-private-class/", CreatePrivateClass.as_view()),
    path("all-public-classes/", PublicClassView.as_view()),
    path("all-private-classes/", PrivateClassView.as_view()),
    path("all-public-classes/<int:pk>/", PublicClassDetailView.as_view()),
    path("all-private-classes/<int:pk>/", PrivateClassDetailView.as_view()),
    path("public-class-update/<int:pk>/", UpdatePublicClass.as_view()),
    path("private-class-update/<int:pk>/", UpdatePrivateClass.as_view()),
    path("add-teacher-to-public-class/<int:pk>/", AddTeacherToPublicClass.as_view()),
    path("add-teacher-to-private-class/<int:pk>/", AddTeacherToPrivateClass.as_view()),
    path("add-mentor-to-public-class/<int:pk>/", AddMentorToPublicClass.as_view()),
    path("add-mentor-to-private-class/<int:pk>/", AddMentorToPrivateClass.as_view()),
    path("students-of-public-class/<int:pk>/", GetStudentsInPublicClass.as_view()),
    path("students-of-private-class/<int:pk>/", GetStudentsInPrivateClass.as_view()),
    path(
        "delete-student-from-public-class/<int:class_id>/<int:student_id>/",
        DeleteStudentFromPublicClass.as_view(),
    ),
    path(
        "delete-student-from-private-class/<int:class_id>/<int:student_id>/",
        DeleteStudentFromPrivateClass.as_view(),
    ),
]
