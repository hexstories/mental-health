# main/views.py
from rest_framework.views import APIView
#from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import SiteInfo, Announcement, Booking
from .serializers import HomePageSerializer, SiteInfoSerializer, AnnouncementSerializer,BookingSerializer

class HomePageView(APIView):
    def get(self, request, format=None):
        site_info = SiteInfo.objects.first()
        announcements = Announcement.objects.all().order_by('-date_posted')

        data = {
            'site_info': SiteInfoSerializer(site_info).data,
            'announcements': AnnouncementSerializer(announcements, many=True).data
        }
        serializer = HomePageSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookingView(APIView):
    def post(self, request, format=None):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    