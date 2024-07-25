from django.contrib import admin
from .models import Counselor, Appointment, BookingAnalytics

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'counselor', 'student', 'date', 'status')
    search_fields = ('counselor__name', 'student', 'status')
    list_filter = ('status', 'date')
    ordering = ('date',)

class BookingAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'counselor', 'total_appointments', 'completed_appointments', 'pending_appointments')
    search_fields = ('counselor__name',)
    list_filter = ('counselor',)
    ordering = ('counselor',)

admin.site.register(Counselor)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(BookingAnalytics, BookingAnalyticsAdmin)
