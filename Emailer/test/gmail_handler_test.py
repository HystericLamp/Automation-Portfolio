import sys
import os
import unittest
from unittest.mock import patch, MagicMock, Mock
import base64

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
        # Build a Mock service
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        # Mock credentials
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

        service = gmailer.authenticate_gmail()

        # Assert that the service is created properly
        self.assertEqual(service, mock_service)
        mock_build.assert_called_once_with('gmail', 'v1', credentials=unittest.mock.ANY)

        mock_open.assert_called_with(os.path.join('data', 'token.json'), 'w')
        mock_open().write.assert_called_once_with('{"token": "valid_token"}')

    @patch('gmail_handler.gmailer.authenticate_gmail')
    def setUp(self, mock_auth):
        """Setup mock service"""
        self.mock_service = Mock()
        mock_auth.return_value = self.mock_service

    def test_fetch_unread_emails_no_emails(self):
        """Testing a gmail fetch when there are no unread emails"""
        self.mock_service.users().messages().list.return_value.execute.return_value = {
            'messages': []
        }

        emails = gmailer.fetch_unread_emails(self.mock_service)
        self.assertEqual(emails, [])

    def test_fetch_unread_emails_with_emails(self):
        """Testing a gmail fetch when there is some unread mail"""
        self.mock_service.users().messages().list.return_value.execute.return_value = {
            'messages': [{'id': '123'}, {'id': '456'}]
        }

        mock_msg_1 = {
            'payload': {
                'headers': [
                    {'name': 'From', 'value': 'sender1@example.com'},
                    {'name': 'Subject', 'value': 'Subject 1'}
                ],
                'parts': [{'mimeType': 'text/plain', 'body': {'data': base64.urlsafe_b64encode(b'Body 1').decode()}}]
            }
        }

        mock_msg_2 = {
            'payload': {
                'headers': [
                    {'name': 'From', 'value': 'sender2@example.com'},
                    {'name': 'Subject', 'value': 'Subject 2'}
                ],
                'parts': [{'mimeType': 'text/plain', 'body': {'data': base64.urlsafe_b64encode(b'Body 2').decode()}}]
            }
        }

        self.mock_service.users().messages().get.side_effect = [
            Mock(execute=Mock(return_value=mock_msg_1)),
            Mock(execute=Mock(return_value=mock_msg_2))
        ]

        emails = gmailer.fetch_unread_emails(self.mock_service)
        self.assertEqual(len(emails), 2)
        self.assertEqual(emails[0], ('sender1@example.com', 'Subject 1', 'Body 1', '123'))
        self.assertEqual(emails[1], ('sender2@example.com', 'Subject 2', 'Body 2', '456'))

    def test_send_gmail_response_success(self):
        """Testing the gmail success response"""
        self.mock_service.users().messages().send.return_value.execute.return_value = {'id': 'abc123'}
        
        with patch('builtins.print') as mock_print:
            gmailer.send_gmail_response(self.mock_service, 'to@example.com', 'Test Subject', 'Test Body')
            mock_print.assert_called_with('Email sent to to@example.com')
    
if __name__ == '__main__':
    unittest.main()