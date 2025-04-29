import unittest
import os
import sys

# Get the absolute path of the src folder and add it to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from gmail_handler import GmailHandler

token_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'token.json')
creds_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'data', 'credentials.json')

class GmailIntegrationTest(unittest.TestCase):
    service = None

    def setUp(self):
        """Set up for integration tests"""
        if GmailIntegrationTest.service is None:
            GmailIntegrationTest.service = GmailHandler.authenticate_gmail()

        self.service = GmailIntegrationTest.service

    def test_real_authenticate_gmail(self):
        """Test real Gmail API authentication and token creation"""

        # Check if token.json is created
        self.assertTrue(os.path.exists(token_path), "token.json was not created!")

        # Verify that the service is created
        self.assertIsNotNone(self.service, "Gmail service not created!")
        self.assertIn('users', dir(self.service), "Gmail service is not properly configured!")

    def test_real_fetch_emails(self):
        """Test fetching real emails from Gmail"""
        self.assertIsNotNone(self.service, "Service is not authenticated!")

        # Fetch unread emails
        messages = GmailHandler.fetch_unread_emails(self.service)
        self.assertIsInstance(messages, list)
        self.assertGreater(len(messages), 0, "No unread emails found!")
        
        # Assert structure of returned message(s)
        self.assertIn('id', messages[0], "Emails should contain an 'id' field")
        self.assertIn('sender', messages[0], "Emails should contain a 'sender' field")
        self.assertIn('subject', messages[0], "Emails should contain a 'subject' field")
        self.assertIn('body', messages[0], "Emails should contain a 'body' field")

    def test_real_send_gmail(self):
        """Test sending a real email via Gmail"""
        self.assertIsNotNone(self.service, "Service is not authenticated!")
        
        recipient = "renzbrian.cruz@gmail.com"
        subject = "Test Email from Automation Script"
        body = "This is a test email to verify sending functionality."

        result = GmailHandler.send_gmail(self.service, recipient, subject, body)
        self.assertTrue(result, "Failed to send the email!")

    # def tearDown(self):
    #     """Clean up after all tests are done"""
    #     if os.path.exists(token_path):
    #         os.remove(token_path)

if __name__ == '__main__':
    unittest.main()