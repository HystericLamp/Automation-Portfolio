import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Get the absolute path of the src folder and add it to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from gmail_handler import gmailer

class GmailTest(unittest.TestCase):
    @patch('gmail_handler.InstalledAppFlow.from_client_secrets_file')
    @patch('gmail_handler.build')
    @patch('gmail_handler.Credentials.from_authorized_user_file')
    @patch('gmail_handler.os.path.exists')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_authenticate_gmail(self, mock_open, mock_path_exists, mock_creds_file, mock_build, mock_flow):
        """Test authentication and service creation"""
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        # Mock valid credentials with a proper to_json() return value
        mock_creds = MagicMock()
        mock_creds.valid = True
        mock_creds.to_json.return_value = '{"token": "valid_token"}'
        mock_creds_file.return_value = mock_creds

        # Mock that token.json exists
        mock_path_exists.return_value = True

        # Mock flow and its run_local_server() if needed
        mock_flow_instance = MagicMock()
        mock_flow.return_value = mock_flow_instance
        mock_flow_instance.run_local_server.return_value = mock_creds

        # Run the authentication
        service = gmailer.authenticate_gmail()

        # Assert that the service is created properly
        self.assertEqual(service, mock_service)
        mock_build.assert_called_once_with('gmail', 'v1', credentials=unittest.mock.ANY)

        # Verify that token.json is written correctly
        mock_open.assert_called_with(os.path.join('data', 'token.json'), 'w')
        mock_open().write.assert_called_once_with('{"token": "valid_token"}')

    
if __name__ == '__main__':
    unittest.main()