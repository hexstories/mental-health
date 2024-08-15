from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("user", "counselor", "date", "status", "created_at")
    list_filter = ("status", "date")
    search_fields = ("user__email", "counselor__name", "status")
    date_hierarchy = "date"
    ordering = ("-date",)
    readonly_fields = ("created_at",)
    
    def has_change_permission(self, request, obj=None):
        if obj and request.user != obj.counselor.user:
            return False
        return super().has_change_permission(request, obj)
    
    def has_delete_permission(self, request, obj=None):
        if obj and request.user != obj.counselor.user:
            return False
        return super().has_delete_permission(request, obj)
