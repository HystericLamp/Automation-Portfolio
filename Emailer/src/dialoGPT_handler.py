import os
from gradio_client import Client

class dialoGPT_handler:
    """
        Class that initializes and handles DialoGPT model interactions and responses.
        Can be used as an interface to DialoGPT model.
    """
    def __init__(self, client_url, api_url, api_token):
        """Connects with HuggingFaces DialoGPT API with Token"""
        self.client_url = client_url
        self.api_url = api_url
        self.api_token = api_token
    
    def get_response(self, prompt):
        """Gets and returns a response from the cloud-hosted DialoGPT model"""
        client = Client(self.client_url, hf_token=self.api_token)
        
        response = client.predict(
            user_input = prompt,
            api_name = self.api_url
        )

        return response