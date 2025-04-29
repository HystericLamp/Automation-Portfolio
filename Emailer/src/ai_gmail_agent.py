from service_factory import ServiceFactory
from gmail_handler import GmailHandler

class AiGmailAgent:
    """
        Class that brings together the Gmail API and AI model API into a smart email responder.
        Also manages the gmail account that sends and recieves mail.
        Acts as an interface to Smart Email Responder app.
    """
    gmail_handler = None
    gmail_service = None
    flan_handler = None

    def __init__(self, gmail_service=None, gmail_handler=None, flan_handler=None):
        # Authenticates and sets up the Gmail Service
        if gmail_service is not None:
            self.gmail_service = gmail_service
        else:
            if AiGmailAgent.gmail_service is None:
                AiGmailAgent.gmail_service = ServiceFactory.create_gmail_service()
            self.gmail_service = AiGmailAgent.gmail_service

        # Instantiates a GmailHandler, which houses gmail operations
        if gmail_handler is not None:
            self.gmail_handler = gmail_handler
        else:
            if AiGmailAgent.gmail_handler is None:
                AiGmailAgent.gmail_handler = ServiceFactory.create_gmail_handler()
            self.gmail_handler = AiGmailAgent.gmail_handler

        # Instantiates a FlanHandler, which calls and handles AI Model API requests
        if flan_handler is not None:
            self.flan_handler = flan_handler
        else:
            if AiGmailAgent.flan_handler is None:
                AiGmailAgent.flan_handler = ServiceFactory.create_flan_handler()
            self.flan_handler = AiGmailAgent.flan_handler

    def get_unread_mail(self):
        """If there is no emails read, returns nothing"""
        emails = self.gmail_handler.fetch_unread_emails(self.gmail_service)
        return emails

    def process_emails(self, emails):
        """Sends a response to every email obtained"""
        if emails is [] or None:
            return
        
        http_code = self.flan_handler.wake_up_space()
        if (http_code == 200):
            for email in emails:
                msg_id = email['id']
                sender = email['sender']
                subject = email['subject']
                body = email['body']

                try:
                    response = self.flan_handler.get_response(body)
                except:
                    print("Problem with getting a response from AI Model occurred")
                    return False

                try:
                    self.gmail_handler.mark_as_read(self.gmail_service, msg_id)
                    self.gmail_handler.send_gmail(self.gmail_service, sender, subject, response)
                except:
                    print("Problem with sending an email occurred")
                    return False

            return True
        
        return False