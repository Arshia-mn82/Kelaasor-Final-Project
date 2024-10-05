from django.urls import path
from .views import *

urlpatterns = [
    path("create-public-class/", CreatePublicClass.as_view()),
    path("create-private-class/", CreatePrivateClass.as_view()),
    path("all-public-classes/", PublicClassView.as_view()),
    path("all-private-classes/", PrivateClassView.as_view()),
    path("all-public-classes/<int:pk>/", PublicClassDetailView.as_view()),
    path("all-private-classes/<int:pk>/", PrivateClassDetailView.as_view()),
    path('public-class-update/<int:pk>/', UpdatePublicClass.as_view()),
    path('private-class-update/<int:pk>/', UpdatePrivateClass.as_view()),
]
