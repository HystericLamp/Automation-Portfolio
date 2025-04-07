import os
import unittest
import requests
from dotenv import load_dotenv

class TestHuggingFaceAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.api_url = os.getenv("HF_MODEL_URL")
        cls.api_token = os.getenv("RHF_API_TOKEN")
        cls.headers = {
            "Authorization": f"Bearer {cls.api_token}",
            "Content-Type": "application/json"
        }

    def test_response_from_model(self):
        payload = { "inputs": "Hello, how are you?" }
        response = requests.post(self.api_url, headers=self.headers, json=payload)

        self.assertEqual(response.status_code, 200, "Expected status code 200")

        try:
            data = response.json()
        except Exception as e:
            self.fail(f"Response is not valid JSON: {e}")

        self.assertIsInstance(data, list)
        self.assertIn("generated_text", data[0], "Missing 'generated_text' in response")


if __name__ == '__main__':
    unittest.main()