from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment
from .serializers import AppointmentSerializer
from ..student.email import send_email
import logging

logger = logging.getLogger(__name__)

class AppointmentView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, "counselor"):
            return Appointment.objects.filter(counselor=self.request.user.counselor)
        return Appointment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        appointment = serializer.save(user=self.request.user)
        counselor_email = appointment.counselor.user.email
        subject = "New Appointment Booked"
        message = f"You have a new appointment with {self.request.user.email} on {appointment.date}."
        send_email(subject, message, counselor_email)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        total_appointments = Appointment.count_total_appointments(request.user)
        completed_appointments = Appointment.count_completed_appointments(request.user)

        logger.debug(f"Total appointments: {total_appointments}")
        logger.debug(f"Completed appointments: {completed_appointments}")

        response.data = {
            "total_appointments": total_appointments,
            "completed_appointments": completed_appointments,
            "appointments": response.data
        }
        return response

class AppointmentStatusUpdateView(generics.UpdateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        appointment = self.get_object()

        if hasattr(request.user, "counselor") and appointment.counselor == request.user.counselor:
            appointment.status = request.data.get("status", appointment.status)
            appointment.save()
            return Response(
                {"status": "success", "message": "Appointment status updated."},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"status": "error", "message": "You do not have permission to update this appointment."},
            status=status.HTTP_403_FORBIDDEN,
        )
