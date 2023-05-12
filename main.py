"""
This models contains an implementation of the finetuned gpt model as a console application
"""

from model_query import get_model_answer
from constants import QUIT_CONSOLE

if __name__ == "__main__":
    print("\033[1;33m" + "Welcome to the QnA system" + "\033[0m")
    while True:
        user_input = input(
            f"BOT >> What would you like to know? --Write {QUIT_CONSOLE} to exit--\n"
        )
        if user_input == QUIT_CONSOLE:
            break
        answer = get_model_answer(user_input)
        if not answer:
            print("BOT >> Sorry I can't answer it, try to reformulate the question")
        else:
            print(f"BOT >> {answer}")
    print("\033[1;33m" + "Thank you for using QnA system" + "\033[0m")
