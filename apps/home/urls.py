# main/urls.py
from django.urls import path
from .views import HomePageView,BookingView


urlpatterns = [
    path('home/', HomePageView.as_view(), name='home-page'),
    path('booking/', BookingView.as_view(), name='booking'),
]
