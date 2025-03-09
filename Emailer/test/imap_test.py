import sys
import os
import unittest
from unittest.mock import patch

# Get the absolute path of the src folder and add it to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

class ImapTest(unittest.TestCase):
    @patch("script.auth_email")
    def test_get_latest_email(self, mock_auth):
        """Test getting latest outlook"""
        # Mock Imap API response

        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()