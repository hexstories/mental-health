from django.urls import path
from .views import (
    chat, 
    conversation_history, 
    delete_conversation_history, 
    delete_specific_conversation, 
    specific_conversation
)

urlpatterns = [
    path(r"chat/", chat, name="chat"),
    path(r"conversation-history/<str:email>/", conversation_history, name="conversation-history"),
    path(r"conversation/<str:email>/", specific_conversation, name="specific_conversation"),
    path(r"conversation/<str:email>/<int:conversation_id>/", specific_conversation, name="specific_conversation_with_id"),
    path(r"conversation/history/<str:email>/delete/", delete_conversation_history, name="delete_conversation_history"),
    path(r"conversation/history/<str:email>/<str:user_message>/delete/", delete_specific_conversation, name="delete_specific_conversation"),
    path(r"delete_conversation/<str:email>/<int:conversation_id>/", delete_specific_conversation, name="delete_specific_conversation_with_id"),
]
