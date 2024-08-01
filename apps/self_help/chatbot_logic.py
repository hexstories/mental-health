import google.generativeai as genai

from dotenv import load_dotenv

import os

import logging

load_dotenv()



class CounsellingSession:
    """
    A class representing a counselling session with a chatbot.

    This class provides methods to generate empathetic responses, practical advice, and follow-up questions
    based on user input.

    Attributes:
        None

    Methods:
        __init__: Initialize the CounsellingSession object.
        generate_response: Generate a response based on user input.

    """

    def __init__(self):
        """
        Initialize the CounsellingSession object.

        This method configures the generative AI with the Google API key and initializes the logger.

        Args:
            None

        Returns:
            None

        """
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)


    def generate_response(self, user_input):
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
                # Function to generate text based on a given prompt
                response = genai.generate_text(prompt=prompt, model="models/text-bison-001")
                return response

            # Generate initial response asking for empathy
            initial_prompt = f"The user says: '{user_input}'. Please respond empathetically and ask clarifying questions if needed."
            initial_text = get_response(initial_prompt)

            # Generate empathetic response
            empathetic_prompt = f"The user shared: '{user_input}'. Craft a response that shows empathy and understanding."
            empathetic_text = get_response(empathetic_prompt)

            # Generate advice response based on user input
            advice_prompt = f"The user says: '{user_input}'. Based on this concern, provide some practical advice or steps they can take to address the issue."
            advice_text = get_response(advice_prompt)

            # Generate follow-up response to the advice given
            follow_up_prompt = f"The user says: '{user_input}'. After providing advice, ask a follow-up question to show continued support and engagement."
            follow_up_text = get_response(follow_up_prompt)

            # Construct the response dictionary
            response = {
                "initial_response": initial_text,
                "empathetic_response": empathetic_text,
                "advice_response": advice_text,
                "follow_up_response": follow_up_text,
            }

            # Log the generated response
            self.logger.info(f"Generated response: {response}")
            return response
        except Exception as e:
            # Log any errors that occur during response generation
            self.logger.error(f"Error generating response: {e}")
            return {"error": str(e)}


if __name__ == "__main__":
    # Testing of the CounsellingSession class
    counselling_session = CounsellingSession()
    # user_input = "I hate me"
    # response = counselling_session.generate_response(user_input)
    # print(response)