import unittest
import os
import sys

# Get the absolute path of the src folder and add it to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gmail_handler import gmailer

token_path = os.path.join(os.path.dirname(__file__), 'data', 'token.json')
creds_path = os.path.join(os.path.dirname(__file__), 'data', 'credentials.json')

class GmailIntegrationTest(unittest.TestCase):
    def setUp(self):
        """Set up for integration tests"""
        # Clean up any existing token.json to start fresh
        if os.path.exists(token_path):
            os.remove(token_path)

    def test_real_authenticate_gmail(self):
        """Test real Gmail API authentication and token creation"""
        service = gmailer.authenticate_gmail()

        # Check if token.json is created
        self.assertTrue(os.path.exists(token_path), "token.json was not created!")

        # Verify that the service is created
        self.assertIsNotNone(service, "Gmail service not created!")
        self.assertIn('users', dir(service), "Gmail service is not properly configured!")
    
    def tearDown(self):
        """Clean up after tests"""
        # Optionally remove token.json after test
        if os.path.exists(token_path):
            os.remove(token_path)

if __name__ == '__main__':
    unittest.main()