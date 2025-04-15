import os
from dotenv import load_dotenv

from gmail_handler import GmailHandler
from flan_handler import FlanHandler

class ServiceFactory:
    """
        Factory class that instantiates and returns gmail API and AI Model API.
    """
    @staticmethod
    def create_gmail_service():
        return GmailHandler.authenticate_gmail()

    @staticmethod
    def create_ai_service():
        load_dotenv()
        client_url = str(os.getenv("HF_SPACE_URL"))
        api_url = str(os.getenv("HF_URL_ENDPOINT"))
        api_token = str(os.getenv("RHF_API_TOKEN"))
        return FlanHandler(
            client_url,
            api_url,
            api_token,
        )