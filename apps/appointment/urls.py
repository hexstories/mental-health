from django.urls import path
from .views import AppointmentView, AppointmentStatusUpdateView

urlpatterns = [
    path('appointments/', AppointmentView.as_view(), name='appointment-list-create'),
    path('appointments/<int:pk>/status/', AppointmentStatusUpdateView.as_view(), name='appointment-status-update'),
]
from django.urls import path
from .views import AppointmentView, AppointmentStatusUpdateView

urlpatterns = [
    path(r"", AppointmentView.as_view(), name="appointment-list-create"),
    path(r"<int:pk>/status/", AppointmentStatusUpdateView.as_view(), name="appointment-status-update"),
]
