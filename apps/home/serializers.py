# main/serializers.py
from rest_framework import serializers
from .models import SiteInfo, Announcement, Booking

class SiteInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteInfo
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

class HomePageSerializer(serializers.Serializer):
    site_info = SiteInfoSerializer()
    announcements = AnnouncementSerializer(many=True)


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'