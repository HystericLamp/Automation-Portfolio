import os
import sys
import unittest
from dotenv import load_dotenv

# Get the absolute path of the src folder and add it to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from ai_gmail_agent import AiGmailAgent

class AiGmailAgentTest(unittest.TestCase):
    agent = None

    @classmethod
    def setUpClass(cls):
        cls.agent = AiGmailAgent()

    def test_email_read_and_respond_process(self):
        emails = self.agent.get_unread_mail()
        self.assertIsInstance(emails, list)
        self.assertGreater(len(emails), 0, "No unread emails found!")

        result = self.agent.process_emails(emails)
        self.assertTrue(result, "Failed to process emails")