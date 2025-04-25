import sys
import os
import unittest
import difflib
from dotenv import load_dotenv

# Get the absolute path of the src folder and add it to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from flan_handler import FlanHandler

# TODO: Change tests to be more consistent with varied responses from model.

class FlanTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.client_api = str(os.getenv("HF_SPACE_API"))
        cls.api_endpoint = str(os.getenv("HF_URL_ENDPOINT"))
        cls.api_token = str(os.getenv("RHF_API_TOKEN"))
        cls.space_url = str(os.getenv("HF_SPACE_URL"))

    def test_flan_space_wake_up(self):
        flan = FlanHandler(self.client_api, self.api_endpoint, self.api_token, self.space_url)
        response_code = flan.wake_up_space()
        self.assertEqual(response_code, 200, f"Failed to wake up space with response code {response_code}")

    def test_flan_basic_response(self):
        prompt = """
            How's the business going?
        """

        flan = FlanHandler(self.client_api, self.api_endpoint, self.api_token, self.space_url)
        response = flan.get_response(prompt)

        expected_response = """
            Hello, I hope you're doing well! We appreciate your business. 
            I'm currently working, which is very competitive. 
            I hope to have a chance to speak with you soon.
        """

        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 10)

        similarity = difflib.SequenceMatcher(None, response.lower(), expected_response.lower()).ratio()

        # Assert similarity threshold
        self.assertGreater(similarity, 0.3, f"Response too different. Got: {response}")


    def test_flan_email_response(self):
        """Tests a response if the prompt is like an email"""
        prompt = """
            Hi, I'm reaching out because I recently purchased a product from your online store and encountered a few issues. 
            First, the package arrived later than expected, which disrupted my schedule since I needed it for an event. 
            Secondly, the item I received was not the same as the one I ordered — it was a different color and lacked a few features that were advertised. 
            I’d appreciate it if someone from your team could look into this matter and let me know how we can resolve it. 
            Thank you.
        """

        flan = FlanHandler(self.client_api, self.api_endpoint, self.api_token, self.space_url)
        response = flan.get_response(prompt)

        expected_response = """
            I’m sorry to hear about the inconvenience. 
            Is the item you purchased the same as the one you ordered? 
            Is there any issue with the product you received?
        """

        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 10)
        
        similarity = difflib.SequenceMatcher(None, response.lower(), expected_response.lower()).ratio()

        # Assert similarity threshold
        self.assertGreater(similarity, 0.3, f"Response too different. Got: {response}")

    def test_multi_turn_conversation(self):
        history = []

        # Turn 1
        user_input_1 = "Hi, I need help with my account."
        flan = FlanHandler(self.client_api, self.api_endpoint, self.api_token, self.space_url)
        response_1 = flan.get_response(user_input_1)
        self.assertIsInstance(response_1, str)
        self.assertGreater(len(response_1), 10)

        # Turn 2
        user_input_2 = "It's not letting me reset my password."
        response_2 = flan.get_response(user_input_2)
        self.assertIsInstance(response_2, str)
        self.assertGreater(len(response_2), 10)
        self.assertNotEqual(response_1, response_2)

        # Turn 3
        user_input_3 = "Can you check if there's a lock on my account?"
        response_3= flan.get_response(user_input_3)
        self.assertIsInstance(response_3, str)
        self.assertIn("account", response_3.lower())

if __name__ == '__main__':
    unittest.main()