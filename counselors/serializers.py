from rest_framework import serializers
from .models import Appointment, BookingAnalytics

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class BookingAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingAnalytics
        fields = '__all__'
