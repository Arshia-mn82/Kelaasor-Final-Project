from django.urls import path
from .views import *

urlpatterns = [
    path(
        "add-task/",
        TaskViewSet.as_view({"post": "create"}),
        name="task-create",
    ),
    path(
        "change-task/<int:pk>/",
        TaskViewSet.as_view({"get": "retrieve", "put": "update"}),
        name="task-detail",
    ),
    path("delete-task/<int:pk>/", TaskViewSet.as_view({"delete": "destroy"})),
    path("add-single-task/", AssignSingleTaskView.as_view(), name="assign_single_task"),
    path("add-group-task/", AssignGroupTaskView.as_view(), name="assign_group_task"),
    path(
        "update-single-task/<int:pk>/",
        UpdateSingleTaskView.as_view(),
        name="update_single_task",
    ),
    path(
        "update-group-task/<int:pk>/",
        UpdateGroupTaskView.as_view(),
        name="update_group_task",
    ),
    path(
        "delete-single-task/<int:pk>/",
        DeleteSingleTaskView.as_view(),
        name="delete_single_task",
    ),
    path(
        "delete-group-task/<int:pk>/",
        DeleteGroupTaskView.as_view(),
        name="delete_group_task",
    ),
    path(
        "get-single-task/<int:pk>/",
        RetrieveSingleTaskView.as_view(),
        name="retrieve_single_task",
    ),
    path(
        "get-group-task/<int:pk>/",
        RetrieveGroupTaskView.as_view(),
        name="retrieve_group_task",
    ),
]
