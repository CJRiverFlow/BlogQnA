"""
This model will evaluate the model with a series of questions
"""

import csv
import nltk
from nltk.translate.bleu_score import sentence_bleu
from transformers import AutoTokenizer, AutoModelWithLMHead

nltk.download("punkt")
tokenizer = AutoTokenizer.from_pretrained("models/fine_tuned_model")
model = AutoModelWithLMHead.from_pretrained("models/fine_tuned_model")


def compute_score(expected_answer, generated_answer):
    expected_answer_tokens = expected_answer.split()
    generated_answer_tokens = generated_answer.split()
    score = sentence_bleu([expected_answer_tokens], generated_answer_tokens)
    return score


# Define a function to generate a response to a given prompt
def generate_response(prompt):
    input_ids = tokenizer.encode(prompt, return_tensors="pt")
    output_ids = model.generate(input_ids)
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response


def test():
    # Load the test data from a CSV file
    with open("data/test_questions.csv", "r") as f:
        reader = csv.DictReader(f)
        test_data = list(reader)

    # Evaluate the model on the test data
    total_score = 0
    for item in test_data:
        question = item["Question"]
        expected_answer = item["Answer"]
        generated_answer = generate_response(question)
        score = compute_score(expected_answer, generated_answer)
        total_score += score

    # Compute the average score
    average_score = total_score / len(test_data)
    return average_score


if __name__ == "__main__":
    average_score = test()

    print(f"Average score: {average_score}")
