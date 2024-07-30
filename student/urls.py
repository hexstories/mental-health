from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView


from .views import (
    ChangePasswordView,
    ForgotPasswordView,
    GoogleLogin,
    ResendVerificationCodeView,
    ResetPasswordView,
    SignUpView,
    UserView,
    VerifyCodeView,
)

router = DefaultRouter()


router.register("users", UserView, basename="users")


urlpatterns = [
    path(r"auth/signup/", SignUpView.as_view(), name="signup"),
    path(r"auth/login/", TokenObtainPairView.as_view(), name="token-obtain"),
    path(r"auth/refresh-token/", TokenRefreshView.as_view(), name="token-refresh"),
    path(
        r"auth/forget-password/", ForgotPasswordView.as_view(), name="forget-password"
    ),
    path(r"auth/reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path(
        r"auth/change-password/", ChangePasswordView.as_view(), name="change-password"
    ),
    path(r"", include(router.urls)),
]
