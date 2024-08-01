from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import UserProfile, Conversation
from .serializers import ConversationSerializer
from .chatbot_logic import CounsellingSession


# Initialize ChatbotLogic with Google AI model
chatbot_logic = CounsellingSession()


@api_view(['POST'])
@permission_classes([AllowAny])
def chat(request):
    """
    Handle chat messages from the user, generate a response using ChatbotLogic,
    and save the conversation to the database.
    """
    email = request.data.get("email")
    user_message = request.data.get("message")

    if not email or not user_message:
        return Response({"error": "Please provide email and message."}, status=status.HTTP_400_BAD_REQUEST)

    user_profile, created = UserProfile.objects.get_or_create(email=email)
    
    response = chatbot_logic.generate_response(user_message)

    # Convert Completion object to string
    response_text = str(response['follow_up_response'].result)

    conversation = Conversation.objects.create(email=email, user_message=user_message, bot_response=response_text)

    return Response({"response": response_text}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def conversation_history(request, email):
    """
    Retrieve the conversation history for a specific user based on email.
    """
    try:
        user_profile = UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    conversations = Conversation.objects.filter(email=email).order_by("timestamp")
    serializer = ConversationSerializer(conversations, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def specific_conversation(request, email, conversation_id=None):
    """
    Retrieve specific conversations for a user based on email and optional query parameters.
    """
    conversation_id = request.query_params.get('conversation_id') or conversation_id
    user_message = request.query_params.get('user_message')

    try:
        user_profile = UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if conversation_id:
        try:
            conversation = Conversation.objects.get(id=conversation_id, email=email)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif user_message:
        conversations = Conversation.objects.filter(email=email, user_message__icontains=user_message).order_by("timestamp")
        if not conversations.exists():
            return Response({"error": "No conversations found with the provided message."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Please provide either 'conversation_id' or 'user_message' as a query parameter."}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_conversation_history(request, email):
    """
    Delete all conversation history for a specific user based on email.
    """
    try:
        user_profile = UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    conversations = Conversation.objects.filter(email=email)
    conversations.delete()

    return Response({"message": "Conversation history deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['DELETE'])
@permission_classes([AllowAny])
def delete_specific_conversation(request, email, conversation_id=None):
    """
    Delete specific conversations for a user based on email and optional query parameters.
    """
    conversation_id = request.query_params.get('conversation_id') or conversation_id
    user_message = request.query_params.get('user_message')

    try:
        user_profile = UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    if conversation_id:
        try:
            conversation = Conversation.objects.get(id=conversation_id, email=email)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)
        conversation.delete()
        return Response({"message": "Conversation deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    elif user_message:
        conversations = Conversation.objects.filter(email=email, user_message__icontains=user_message)
        if not conversations.exists():
            return Response({"error": "No conversations found with the provided message."}, status=status.HTTP_404_NOT_FOUND)
        conversations.delete()
        return Response({"message": "Conversations deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"error": "Please provide either 'conversation_id' or 'user_message' as a query parameter."}, status=status.HTTP_400_BAD_REQUEST)