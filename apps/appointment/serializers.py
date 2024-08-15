from rest_framework import serializers
from .models import Appointment
from django.utils import timezone

class AppointmentSerializer(serializers.ModelSerializer):
    counselor_name = serializers.CharField(source="counselor.name", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Appointment
        fields = [
            "id",
            "user",
            "user_email",
            "counselor",
            "counselor_name",
            "date",
            "created_at",
            "status",
        ]
        read_only_fields = ["id", "created_at", "status"]

    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("The appointment date must be in the future.")
        return value
