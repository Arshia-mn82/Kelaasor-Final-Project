from django.urls import path
from .views import *

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view() , name="login"),
    path('all_users/' , AccountListView.as_view()),
    path('update/<int:id>/', AccountDetailView.as_view(), name='account_detail'),
]