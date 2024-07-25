from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment, BookingAnalytics
from .serializers import AppointmentSerializer, BookingAnalyticsSerializer

class AppointmentListView(APIView):
    def get(self, request, counselor_id):
        appointments = Appointment.objects.filter(counselor_id=counselor_id)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

class BookingAnalyticsView(APIView):
    def get(self, request, counselor_id):
        try:
            analytics = BookingAnalytics.objects.get(counselor_id=counselor_id)
            serializer = BookingAnalyticsSerializer(analytics)
            return Response(serializer.data)
        except BookingAnalytics.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
