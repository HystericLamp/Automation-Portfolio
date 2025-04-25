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
    def create_gmail_handler():
        return GmailHandler()

    @staticmethod
    def create_flan_handler():
        load_dotenv()
        client_api = str(os.getenv("HF_SPACE_API"))
        api_endpoint = str(os.getenv("HF_URL_ENDPOINT"))
        api_token = str(os.getenv("RHF_API_TOKEN"))
        space_url = str(os.getenv("HF_SPACE_URL"))

        return FlanHandler(
            client_api,
            api_endpoint,
            api_token,
            space_url
        )