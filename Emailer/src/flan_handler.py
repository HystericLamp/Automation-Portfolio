import requests
from gradio_client import Client

class FlanHandler:
    """
        Class that initializes and handles flan-t5-large model interactions and responses.
        Can be used as an interface to flan-t5-large model.
    """
    def __init__(self, client_api, api_endpoint, api_token, space_url):
        """Connects with Google's Flan API on Hugging Faces with Token"""
        self.client_api = client_api
        self.api_endpoint = api_endpoint
        self.api_token = api_token
        self.space_url = space_url

    def wake_up_space(self):
        """Pings space to wake it up and then returns status code"""
        print(f"Pinging {self.space_url} to wake up the Space...")

        try:
            r = requests.get(self.space_url, timeout=60)
            if r.status_code == 200:
                print("Space is up!")
            else:
                print(f"Space responded with status: {r.status_code}")
        except requests.exceptions.Timeout:
            print("Space is starting... took too long to respond")

        return r.status_code
    
    def get_response(self, input):
        """Gets and returns a response from the cloud-hosted Flan model"""
        client = Client(self.client_api, hf_token=self.api_token)
        
        response = client.predict(
            prompt = input,
            api_name = self.api_endpoint
        )

        return response