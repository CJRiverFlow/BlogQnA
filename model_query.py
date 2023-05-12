"""
This file contains the functions needed to utilize the model and get the output response
"""

from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelWithLMHead
from constants import TRAINED_MODEL_PATH, BASE_MODEL

tokenizer = AutoTokenizer.from_pretrained(TRAINED_MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(TRAINED_MODEL_PATH)

def get_model_answer(user_input: str) -> str:
    # encode the user input and generate a response
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    chat_response_ids = model.generate(
        input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id
    )

    # decode the response and remove the input from the chat response
    chat_response = tokenizer.decode(chat_response_ids[0], skip_special_tokens=True)
    chat_response = chat_response[len(user_input) :].strip()

    return chat_response
