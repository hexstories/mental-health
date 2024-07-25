from django.urls import path
from .views import AppointmentListView, BookingAnalyticsView

urlpatterns = [
    path('appointments/<int:counselor_id>/', AppointmentListView.as_view(), name='appointments-list'),
    path('analytics/<int:counselor_id>/', BookingAnalyticsView.as_view(), name='booking-analytics'),
]
