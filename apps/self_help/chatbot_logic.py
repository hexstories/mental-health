import google.generativeai as genai
from dotenv import load_dotenv
import os
import logging
import asyncio
from django.core.cache import cache

load_dotenv()


class CounsellingSession:
    """
    A class representing a counselling session with a chatbot.

    This class provides methods to generate empathetic responses, practical advice, and follow-up questions
    based on user input.
    """

    def __init__(self):
        """
        Initialize the CounsellingSession object.
        Configures the generative AI with the Google API key and initializes the logger.
        """
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    async def generate_response(self, user_input):
        """
        Generate a response based on user input.
        This method generates an initial empathetic response, followed by advice and a follow-up question.

        Args:
            user_input (str): The input provided by the user.

        Returns:
            dict: A dictionary containing the generated responses.
        """
        try:
            def get_response(prompt):
                response = genai.generate_text(prompt=prompt, model="models/text-bison-001")
                return response

            # Cache key based on the user input
            cache_key = f"response_{hash(user_input)}"
            cached_response = cache.get(cache_key)

            if cached_response:
                self.logger.info("Returning cached response")
                return cached_response

            # Prepare prompts
            prompts = [
                f"The user says: '{user_input}'. Please respond empathetically and ask clarifying questions if needed.",
                f"The user shared: '{user_input}'. Craft a response that shows empathy and understanding.",
                f"The user says: '{user_input}'. Based on this concern, provide some practical advice or steps they can take to address the issue.",
                f"The user says: '{user_input}'. After providing advice, ask a follow-up question to show continued support and engagement."
            ]

            # Asynchronously generate responses
            tasks = [get_response(prompt) for prompt in prompts]
            responses = await asyncio.gather(*tasks)

            response = {
                "initial_response": responses[0],
                "empathetic_response": responses[1],
                "advice_response": responses[2],
                "follow_up_response": responses[3],
            }

            self.logger.info(f"Generated response: {response}")
            cache.set(cache_key, response, timeout=300)  # Cache for 5 minutes

            return response

        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return {"error": str(e)}
