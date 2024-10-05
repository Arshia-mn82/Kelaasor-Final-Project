from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from rest_framework.generics import ListAPIView
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated
from .forms import *
from django.shortcuts import render, redirect


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        form = RegisterForm()
        return render(request, "account/register.html", {"form": form})

    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():

            new_user = User.objects.create(
                username=form.cleaned_data["email"],
                email=form.cleaned_data["email"],
                password=make_password(form.cleaned_data["password"]),
            )

            account = Account(
                user=new_user,
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                phone_number=form.cleaned_data["phone_number"],
                email=form.cleaned_data["email"],
                password=make_password(form.cleaned_data["password"]),
            )
            account.save()
            return redirect("login")
        return render(request, "account/register.html", {"form": form})


class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        form = LoginForm()
        return render(request, "account/login.html", {"form": form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            try:
                account = Account.objects.get(email=email)

                if check_password(password, account.password):
                    refresh = RefreshToken.for_user(account.user)
                    return Response(
                        {"refresh": str(refresh), "access": str(refresh.access_token)}
                    )

                return render(
                    request,
                    "account/login.html",
                    {"form": form, "error": "Invalid credentials"},
                )
            except Account.DoesNotExist:
                return render(
                    request,
                    "account/login.html",
                    {"form": form, "error": "Invalid credentials"},
                )
        return render(request, "account/login.html", {"form": form})


class AccountListView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountListSerializer


class AccountDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return Account.objects.get(id=id)
        except Account.DoesNotExist:
            return None

    def get(self, request, id):
        account = self.get_object(id)
        if account:
            serializer = AccountUpdateSerializer(account)
            return Response(serializer.data)
        return Response(
            {"detail": "Account not found"}, status=status.HTTP_404_NOT_FOUND
        )

    def put(self, request, id):
        account = self.get_object(id)
        if account:
            if account.user != request.user:
                return Response(
                    {"detail": "You do not have permission to update this account."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            serializer = AccountUpdateSerializer(
                account, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"detail": "Account not found"}, status=status.HTTP_404_NOT_FOUND
        )

    def delete(self, request, id):
        account = self.get_object(id)
        if account:
            if account.user != request.user:
                return Response(
                    {"detail": "You do not have permission to delete this account."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            account.delete()
            return Response(
                {"detail": "Account deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            {"detail": "Account not found"}, status=status.HTTP_404_NOT_FOUND
        )
