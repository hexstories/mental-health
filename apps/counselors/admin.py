from django.contrib import admin
from .models import  Counselor

@admin.register(Counselor)
class CounselorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'department')
    search_fields = ('name', 'email', 'department')
    list_filter = ('department',)
