from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuestionSerializer
from django.conf import settings
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

#load model

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history =[])


def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

class QnAView(APIView):
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.validated_data['question']
            try:
                response = get_gemini_response(question)
                response_text = "".join(chunk.text for chunk in response)
                return Response({"question": question, "answer": response_text}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



#initialize streamlit
st.set_page_config(page_title="Q&A Demo")

st.header("University Councelling Center")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

input = st.text_input("Input:", key="input")
submit = st.button("Ask the question")

if submit and input:
    response = get_gemini_response(input)
    st.session_state['chat_history'].append(("You",input))
    st.subheader("The response is ")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(("Bot",chunk.text))
st.subheader("The Chat history is")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")    