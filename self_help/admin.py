from django.contrib import admin
from .models import UserProfile, Conversation


admin.site.register(UserProfile)
admin.site.register(Conversation)