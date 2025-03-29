import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class dialoGPT_handler:
    """
    Class that initializes and handles DialoGPT model interactions and responses
    """
    def __init__(self):
        # Load DialoGPT model and tokenizer
        self.model_name = "microsoft/DialoGPT-medium"
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)

        self.chat_history_ids = None
    
    def get_response(self, prompt):
        """Gets and returns a response from the AI model"""
        new_input_ids = self.tokenizer.encode(prompt + self.tokenizer.eos_token, return_tensors="pt")
        if self.chat_history_ids is not None:
            input_ids = torch.cat([self.chat_history_ids, new_input_ids], dim=-1)
        else:
            input_ids = new_input_ids
        
        
        attention_mask = input_ids.ne(self.tokenizer.pad_token_id).long()

        output_ids = self.model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=50,
            pad_token_id=self.tokenizer.eos_token_id,
            num_return_sequences=1,
            temperature=0.0,
            do_sample=False,
            num_beams=3,
        )

        self.chat_history_ids = output_ids
        reply = self.tokenizer.decode(output_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

        return reply