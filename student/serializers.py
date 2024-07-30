from random import choices
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils import timezone
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .email import send_email
from .utils import OTPUtils


User = get_user_model()

PASSWORD_MIN_LENGTH = 8


class SignUpSerializer(serializers.ModelSerializer):
    """
    Serializer for signing up a new user
    """

    password = serializers.CharField(min_length=PASSWORD_MIN_LENGTH, write_only=True)
    password2 = serializers.CharField(min_length=PASSWORD_MIN_LENGTH, write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone_number",
            "password",
            "password2",
        ]

    # Check if passwords match
    def validate_password2(self, password2: str):
        if self.initial_data.get("password") != password2:
            raise serializers.ValidationError("Passwords do not match")
        return password2

    def create(self, validated_data: dict):
        if User.objects.filter(
            email=validated_data["email"], is_verified=True
        ).exists():
            raise serializers.ValidationError(
                {"detail": "User with this email already exists"}
            )

        validated_data.pop("password2")
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class SignupResponseSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "phone_number", "email", "token")

    @swagger_serializer_method(
        serializer_or_field=serializers.JSONField(),
    )
    def get_token(self, user: User):
        refresh = RefreshToken.for_user(user)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "id"]


class ForgotPasswordSerializer(serializers.Serializer):
    """Serializer for initiating forgot password. Send reset code"""

    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        if not email:
            raise serializers.ValidationError("Email must be provided")
        return attrs

    def create(self, validated_data: dict):
        """Send an email with a code to reset the password"""
        email = validated_data.get("email")

        try:
            user = User.objects.filter(email=email).first()
            if user:
                code, token = OTPUtils.generate_otp(user)
                send_mail("Password Reset", code, email)
                #subject, message, recipient
            else:
                raise serializers.ValidationError("User with this email does not exist")
        except Exception as e:
            raise serializers.ValidationError(f"Error sending email: {e}")

        return {"message": "verification code sent successfully", "token": token}


class ResetPasswordSerializer(serializers.Serializer):
    """ """

    token = serializers.CharField(required=True)
    code = serializers.CharField(min_length=6, required=True)
    password = serializers.CharField(min_length=PASSWORD_MIN_LENGTH, required=True)

    def create(self, validated_data):
        """
        Reset user password using email as an identification
        """

        token = validated_data.get("token")
        code = validated_data.get("code")
        password = validated_data.get("password")

        data = OTPUtils.decode_token(token)

        if not data or not isinstance(data, dict):
            raise serializers.ValidationError("Invalid token")

        if not (user := User.objects.filter(id=data.get("user_id")).first()):
            raise serializers.ValidationError("User does not exist")

        # validate code
        if not OTPUtils.verify_otp(code, data["secret"]):
            raise serializers.ValidationError("Invalid code")

        # reset password
        user.set_password(raw_password=password)
        user.save()

        return {
            "email": user.email,
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(min_length=PASSWORD_MIN_LENGTH, required=True)
    new_password = serializers.CharField(min_length=PASSWORD_MIN_LENGTH, required=True)

    class Meta:
        fields = ("old_password", "new_password")

    def create(self, validated_data):
        request = self.context.get("request")
        user: User = request.user

        if not user.check_password(validated_data.get("old_password")):
            raise serializers.ValidationError({"detail": "Incorrect password"})

        # reset password
        user.set_password(raw_password=validated_data.get("new_password"))
        user.save()

        return {"old_password": "", "new_password": ""}

 
