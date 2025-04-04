import os.path
import sys
import base64
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

creds_path = os.path.join(os.path.dirname(__file__), 'data', 'credentials.json')
token_path = os.path.join(os.path.dirname(__file__), 'data', 'token.json')

class gmailer:
    """
        Class that handles gmail API requests and operations on gmail
    """
    def authenticate_gmail():
        """authorize the application and generate a token.json file for future API requests"""
        creds = None

        data_folder = os.path.dirname(token_path)
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

        # Check if token.json already exists
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path)

        # If no valid credentials available, authenticate user
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # Load credentials.json (OAuth file)
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                creds = flow.run_local_server(port=0)

        # Save token for future use
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    def fetch_unread_emails(service):
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

                # Extract sender and subject
                sender = next(header['value'] for header in headers if header['name'] == 'From')
                subject = next(header['value'] for header in headers if header['name'] == 'Subject')
                
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
                    'sender': sender,
                    'subject': subject,
                    'body': body
                })

        return emails
    
    def send_gmail_response(service, to_email, subject, body):
        message = MIMEText(body)
        message['to'] = to_email
        message['subject'] = subject

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        create_message = {'raw': encoded_message}

        # Send the email
        send_message = service.users().messages().send(userId="me", body=create_message).execute()
        return send_message