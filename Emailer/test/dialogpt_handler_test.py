import sys
import os
import unittest
import difflib
from dotenv import load_dotenv

# Get the absolute path of the src folder and add it to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from dialoGPT_handler import dialoGPT_handler

class DialoGPTTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.api_url = str(os.getenv("HF_URL_ENDPOINT"))
        cls.api_token = str(os.getenv("RHF_API_TOKEN"))
        cls.client_url = str(os.getenv("HF_SPACE_URL"))

    def test_dialogpt_response(self):
        """Tests the response from DialoGPT"""
        prompt = "I got a burn on my hand yesterday."

        dialo = dialoGPT_handler(self.client_url, self.api_url, self.api_token)
        response = dialo.get_response(prompt)

        print(f"Prompt: {prompt}")
        print(f"Response: {response}")

        expected_response = "Oh no, are you alright?"
        similarity = difflib.SequenceMatcher(None, response.lower(), expected_response.lower()).ratio()

        # Assert similarity threshold
        self.assertGreater(similarity, 0.7, f"Response too different. Got: {response}")


if __name__ == '__main__':
    unittest.main()