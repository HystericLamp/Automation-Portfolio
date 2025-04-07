import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
from dotenv import load_dotenv

"""
    Setup to build required files for Hugging Face's model repo
    Will need a token with WRITE access
"""

load_dotenv()
API_TOKEN: str = os.getenv("WHF_API_TOKEN")
login(API_TOKEN)

model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")

MODEL: str = os.getenv("MODEL")
TOKENIZER: str = os.getenv("TOKENIZER")
model.push_to_hub(MODEL)
tokenizer.push_to_hub(TOKENIZER)