from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from .models import Appointment,Counselor
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import AppointmentSerializer,CounselorSerializer

class AppointmentListView(APIView):
    def get(self, request, counselor_id):
        appointments = Appointment.objects.filter(counselor_id=counselor_id)
        self.permission_classes = [IsAuthenticated]
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    

class CounselorViewSet(viewsets.ModelViewSet):
    queryset = Counselor.objects.all()
    serializer_class = CounselorSerializer
    http_method_names = [m for m in viewsets.ModelViewSet.http_method_names if m != 'put']

    def perform_create(self, serializer):
        return super().perform_create(serializer)
    
    def get_permissions(self):
        if self.action in ['update','partial_update', 'destory',]:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions() 
            

# class BookingAnalyticsView(APIView):
#     def get(self, request, counselor_id):
#         try:
#             analytics = BookingAnalytics.objects.get(counselor_id=counselor_id)
#             serializer = BookingAnalyticsSerializer(analytics)
#             return Response(serializer.data)
#         except BookingAnalytics.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
