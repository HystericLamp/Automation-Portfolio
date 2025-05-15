import os.path
import base64
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from email.mime.text import MIMEText
from dotenv import load_dotenv

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

load_dotenv()
if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
    creds_path = os.path.join(os.path.dirname(__file__), 'data', 'credentials.json')
    token_path = "/tmp/token.json"
else:
    tmp_dir = os.path.join(os.path.dirname(__file__), 'data')
    creds_path = os.path.join(tmp_dir, 'credentials.json')
    token_path = os.path.join(tmp_dir, 'token.json')

class GmailHandler:
    """
        Class that handles gmail API requests and operations on gmail
    """
    
    @staticmethod
    def authenticate_gmail():
        """
            Authorize the application and generate a token.json file for future API requests
        """
        creds = None

        data_folder = os.path.dirname(token_path)
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        # Check if token.json already exists
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path)

        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print("Refresh failed, removing old token and retrying authentication:", e)
                os.remove(token_path)
                return GmailHandler.authenticate_gmail()
        elif not creds or not creds.valid:
            if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
                raise RuntimeError("No valid token.json and cannot run OAuth flow in AWS Lambda.")
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, ['https://www.googleapis.com/auth/gmail.modify'])
            creds = flow.run_local_server(port=0)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        # Save token for future use
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)
    
    def mark_as_read(self, service, msg_id):
        """Mark an email as read by removing the UNREAD label."""
        service.users().messages().modify(
            userId='me',
            id=msg_id,
            body={'removeLabelIds': ['UNREAD']}
        ).execute()

        return True

    def fetch_unread_emails(self, service):
        """Fetch unread emails from gmail account"""
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
        messages = results.get('messages', [])

        emails = []
        if not messages:
            print("No unread emails found.")
        else:
            for msg in messages:
                msg_id = msg['id']
                msg_data = service.users().messages().get(userId='me', id=msg_id, format='full').execute()

                payload = msg_data['payload']
                headers = payload['headers']

                # Extract any relevant data
                sender = next(header['value'] for header in headers if header['name'] == 'From')
                subject = next(header['value'] for header in headers if header['name'] == 'Subject')
                thread_id = msg_data['threadId']
                message_id = next((header['value'] for header in headers if header['name'] == 'Message-ID'), None)

                # Get email body
                body = ""
                if 'parts' in payload:
                    for part in payload['parts']:
                        if part['mimeType'] == 'text/plain':
                            body = part['body']['data']
                            break

                if body:
                    import base64
                    body = base64.urlsafe_b64decode(body).decode('utf-8')
                
                # Append email to list as a dictionary
                emails.append({
                    'id': msg_id,
                    'thread_id': thread_id,
                    'message_id': message_id,
                    'sender': sender,
                    'subject': subject,
                    'body': body
                })

        return emails
    
    def send_gmail(self, service, to_email, subject, body):
        message = MIMEText(body)
        message['to'] = to_email
        message['subject'] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}

        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        return send_message
    
    def send_gmail_reply(self, service, to_email, subject, body, thread_id, message_id):
        message = MIMEText(body)
        message['to'] = to_email
        message['subject'] = f"Re: {subject}"
        message['In-Reply-To'] = message_id
        message['References'] = message_id

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {
            'raw': encoded_message,
            'threadId': thread_id
        }

        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        return send_message