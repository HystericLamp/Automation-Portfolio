import sys
import os
import unittest
import difflib

# Get the absolute path of the src folder and add it to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from dialoGPT_handler import dialoGPT_handler

class DialoGPTTest(unittest.TestCase):
    def test_dialogpt_response(self):
        prompt = "Hello, how are you doing today?"

        dialo = dialoGPT_handler()
        response = dialo.get_response(prompt)

        print(f"Prompt: {prompt}")
        print(f"Response: {response}")

        expected_response = "Doing great myself! How about you?"
        similarity = difflib.SequenceMatcher(None, response.lower(), expected_response.lower()).ratio()

        # Assert similarity threshold
        self.assertGreater(similarity, 0.5, f"Response too different. Got: {response}")


if __name__ == '__main__':
    unittest.main()