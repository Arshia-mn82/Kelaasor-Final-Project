from django.urls import path
from .views import PublicClassView, PrivateClassView

urlpatterns = [
    path("public-class/", PublicClassView.as_view(), name="public-class-create"),
    path(
        "public-class/<int:pk>/",
        PublicClassView.as_view(),
        name="public-class-update-delete",
    ),
    path("private-class/", PrivateClassView.as_view(), name="private-class-create"),
    path(
        "private-class/<int:pk>/",
        PrivateClassView.as_view(),
        name="private-class-update-delete",
    ),
]
