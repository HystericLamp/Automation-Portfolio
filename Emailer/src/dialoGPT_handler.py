import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests
import json

class dialoGPT_handler:
    """
    Class that initializes and handles DialoGPT model interactions and responses
    """
    def __init__(self, api_url, api_token):
        """Connects with HuggingFaces DialoGPT API with Token"""
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

        self.chat_history = []
    
    def get_response(self, prompt):
        """Gets and returns a response from the cloud-hosted DialoGPT model"""
        self.chat_history.append({"role": "user", "content": prompt})

        payload = {
            "inputs": {"text": prompt},
            "parameters": {
                "max_length": 50,
                "temperature": 0.7,
                "do_sample": True,
                "num_return_sequences": 1,
            },
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            generated_text = result['generated_text']
            self.chat_history.append({"role": "assistant", "content": generated_text})
            return generated_text
        else:
            return f"Error: {response.status_code}, {response.text}"