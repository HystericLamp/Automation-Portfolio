from service_factory import ServiceFactory

class AiGmailAgent:
    """
        Class that brings together the Gmail API and AI model API into a smart email responder.
        Also manages the gmail account that sends and recieves mail.
    """
    gmail_service = None
    ai_service = None

    def __init__(self, gmail_service=None, ai_service=None):
        if gmail_service is not None:
            self.gmail_service = gmail_service
        else:
            if AiGmailAgent.gmail_service is None:
                AiGmailAgent.gmail_service = ServiceFactory.create_gmail_service()
            self.gmail_service = AiGmailAgent.gmail_service

        if ai_service is not None:
            self.ai_service = ai_service
        else:
            if AiGmailAgent.ai_service is None:
                AiGmailAgent.ai_service = ServiceFactory.create_ai_service()
            self.ai_service = AiGmailAgent.ai_service

    def send_email(self):
        print()

    def read_email(self):
        print()