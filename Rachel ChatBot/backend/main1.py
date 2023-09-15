import openai
import json
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

choices = [
    "get account balance",
    "pay my bill",
    "schedule an appointment",
    "change an appointment",
    "cancel an appointment",
    "lookup next appointment",
    "cancel subscription",
    "talk to an agent"
]

responses = [
    "Your balance is $150.00, due on September 30, 2023.",
    "You can pay your bill online by going to www.goaptive.com.",
    "The following appointment slots are available.",
    "Please call 888-888-8888 to re-schedule your appointment.",
    "Your appointment has been cancelled.",
    "Your next appointment is on October 3, 2023 between 10 am and 12 pm",
    "I'm sorry. Cancelling your subscription is not possible. We own you!!!",
    "We don't allow real people to talk to customers any more."
]

def ask_gpt3(prompt):
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)

def write_db(data):
    with open("interactions.json", "w") as db_file:
        json.dump(data, db_file)

def read_db():
    try:
        with open("interactions.json", "r") as db_file:
            return json.load(db_file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"interactions": []}

def get_response_from_choice(choice):
    return responses[choices.index(choice)]

def main():
    while True:
        user_input = input("\nHow can I assist you? (or type 'exit' to quit): ")

        if user_input == "exit":
            break

        # Attempt to understand user's input via GPT-3
        predicted_intent = ask_gpt3(user_input)
        if predicted_intent in choices:
            response = get_response_from_choice(predicted_intent)
            print(response)
        else:
            # If the intent is not clearly understood, present a list of choices to the user.
            print("\nSorry, I couldn't understand your request. Please choose from the options below:")
            for idx, choice in enumerate(choices, 1):
                print(f"{idx}. {choice}")

            choice_input = input("\nYour choice (1-8): ")
            try:
                selected_idx = int(choice_input) - 1
                if 0 <= selected_idx < 8:
                    response = responses[selected_idx]
                    print(response)
                else:
                    print("Invalid choice. Please choose a number between 1 and 8.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 8.")
        
        # Record interaction
        current_data = read_db()
        current_data["interactions"].append({
            "user_input": user_input,
            "response": response
        })
        write_db(current_data)

        # Check if user wants to continue
        cont = input("\nDo you need further assistance? (yes/no): ").strip().lower()
        if cont == 'no':
            break

if __name__ == "__main__":
    main()
