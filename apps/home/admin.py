# main/admin.py
from django.contrib import admin
#from django.core.exceptions import PermissionDenied
from .models import SiteInfo, Announcement, Booking
from django.contrib.auth.models import User, Group

class SiteInfoAdmin(admin.ModelAdmin):
    list_display = ('office_location', 'contact_number', 'office_visit_info')

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_posted')
    search_fields = ('title',)
    list_filter = ('date_posted',)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'booking_date')
    search_fields = ('full_name', 'email')
    list_filter = ('booking_date',)

    



admin.site.register(SiteInfo, SiteInfoAdmin)
admin.site.register(Announcement, AnnouncementAdmin)
admin.site.register(Booking, BookingAdmin)
