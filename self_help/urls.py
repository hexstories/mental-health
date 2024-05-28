from django.urls import path
from .views import QnAView

urlpatterns = [
    path('self_help/', QnAView.as_view(), name='ask'),
]
