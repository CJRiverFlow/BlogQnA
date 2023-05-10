"""
This script contains the process for training the machine learning model
"""

import torch
import argparse
from torch.optim import AdamW
from transformers import AutoTokenizer, AutoModelWithLMHead


def train(epochs: int, device: str):
    tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    model = AutoModelWithLMHead.from_pretrained("microsoft/DialoGPT-medium")

    # Load your training data from a text file
    with open("data/blogposts.txt", "r") as f:
        train_data = f.read().split("\n")

    # Set the pad_token attribute of the tokenizer to the eos_token
    tokenizer.pad_token = tokenizer.eos_token

    # Define the optimizer
    optimizer = AdamW(model.parameters(), lr=5e-5)

    # Encode the data
    input_ids = tokenizer(
        train_data, return_tensors="pt", padding=True, truncation=True
    )["input_ids"]

    # Move the model and data to the specified device
    model.to(device)
    input_ids = input_ids.to(device)

    # Fine-tune the model
    print("--- Starting training process ---")
    model.train()
    for epoch in range(epochs):
        print(f"Epoch: {epoch+1}/{epochs}")
        for batch_num, batch in enumerate(input_ids):
            outputs = model(batch, labels=batch)
            loss = outputs.loss
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            print(f"Batch: {batch_num+1}/{len(input_ids)}, Loss: {loss.item()}")

    # Save the fine-tuned model
    model.save_pretrained("models/fine_tuned_model")
    tokenizer.save_pretrained("models/fine_tuned_model")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This script is for training the machine learning model"
    )
    parser.add_argument("--epochs", type=int, help="number of training epochs")
    parser.add_argument("--gpu", action='store_true', help="use gpu for training")
    args = parser.parse_args()

    device = torch.device("cuda" if args.gpu and torch.cuda.is_available() else "cpu")
    print(f"Starting training process on {device}")
    train(args.epochs, device)
