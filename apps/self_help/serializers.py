from rest_framework import serializers
from .models import Conversation

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = [
            "email", 
            "user_message", 
            "bot_response", 
            "timestamp"
    ]
