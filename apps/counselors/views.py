from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets, permissions
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import generics 
from .models import Counselor




from .serializers import (
    CounselorSignUpSerializer, CounselorSignupResponseSerializer,
    CounselorForgotPasswordSerializer, CounselorResetPasswordSerializer,
    CounselorChangePasswordSerializer, CounselorSerializer  
)

response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "message": openapi.Schema(type=openapi.TYPE_STRING),
    },
)

forget_password_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={"token": openapi.Schema(type=openapi.TYPE_STRING)},
)



class CounselorSignUpView(CreateAPIView):
    serializer_class = CounselorSignUpSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="User signup with email verification",
        responses={201: CounselorSignupResponseSerializer},
    )
    def create(self, request, *args, **kwargs):
        # Create the user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
           status=status.HTTP_201_CREATED
        )


class CounselorForgotPasswordView(CreateAPIView):
    serializer_class = CounselorForgotPasswordSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Send reset code to the user's email",
        responses={200: forget_password_schema},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response(data, status=status.HTTP_200_OK)


class CounselorResetPasswordView(CreateAPIView):
    serializer_class = CounselorResetPasswordSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Reset user password using the code sent to email",
        responses={200: response_schema},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Password reset successfully"}, status=status.HTTP_200_OK
        )


class CounselorChangePasswordView(CreateAPIView):
    serializer_class = CounselorChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Change password for authenticated user",
        responses={200: response_schema},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "Password changed successfully"}, status=status.HTTP_200_OK
        )



class CounselorDetailView(generics.RetrieveUpdateAPIView):
    queryset = Counselor.objects.all()
    serializer_class = CounselorSerializer
    permission_classes = [IsAuthenticated]