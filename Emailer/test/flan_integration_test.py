import os
import unittest
from dotenv import load_dotenv
from gradio_client import Client
import difflib

class TestHuggingFaceAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.api_url = str(os.getenv("HF_URL_ENDPOINT"))
        cls.api_token = str(os.getenv("RHF_API_TOKEN"))
        cls.client_api = str(os.getenv("HF_SPACE_API"))
        cls.space_url = str(os.getenv("HF_SPACE_URL"))

    def test_response_from_model(self):
        # Call the API
        client = Client(self.client_api, hf_token=self.api_token)
        
        response = client.predict(
            prompt = "Hello, how are you?",
            api_name = self.api_url
        )
        
        # Check Similarity of response to desired
        expected_response = "I'm good, how are you?"
        similarity = difflib.SequenceMatcher(None, response.lower(), expected_response.lower()).ratio()

        self.assertGreater(similarity, 0.3, f"Response too different. Got: {response}")

if __name__ == '__main__':
    unittest.main()
