from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
   CounselorSignUpView,
    CounselorDetailView, CounselorForgotPasswordView,
    CounselorResetPasswordView, CounselorChangePasswordView,
)

router = DefaultRouter()
router.register(r'counselors', CounselorDetailView, basename='counselor')

urlpatterns = [
    path('signup/', CounselorSignUpView.as_view(), name='signup'),
   # path('user/<int:pk>/', UserView.as_view(), name='user-detail'),
    path('counselor/<int:pk>/', CounselorDetailView.as_view(), name='counselor-detail'),
    path('forgot-password/', CounselorForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', CounselorResetPasswordView.as_view(), name='reset-password'),
    path('change-password/', CounselorChangePasswordView.as_view(), name='change-password'),
]
