import openai
import json
from dotenv import load_dotenv
import os

load_dotenv()

openai.api_key = os.getenv("APIKEY")

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

responses = {
    "get account balance": "Your balance is $150.00, due on September 30, 2023.",
    "pay my bill": "You can pay your bill online by going to www.goaptive.com.",
    "schedule an appointment": "The following appointment slots are available.",
    "change an appointment": "Please call 888-888-8888 to re-schedule your appointment.",
    "cancel an appointment": "Your appointment has been cancelled.",
    "lookup next appointment": "Your next appointment is on October 3, 2023 between 10 am and 12 pm",
    "cancel subscription": "I'm sorry. Cancelling your subscription is not possible. We own you!!!",
    "talk to an agent": "We don't allow real people to talk to customers any more."
}

def ask_gpt3(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150  # you can adjust this number as you see fit
    )
    return response.choices[0].message['content'].strip()

def map_to_choice(interpretation):
    for choice in choices:
        if any(word in interpretation for word in choice.split()):
            return choice
    return None


def write_to_db(data):
    with open("database.py", "w") as db_file:
        json.dump(data, db_file, indent=4)

def read_db():
    try:
        with open("database.py", "r") as db_file:
            return json.load(db_file)
    except FileNotFoundError:
        return {"interactions": []}

def main():
    while True:
        user_input = input("Hello! How can I assist you today? ")
        if user_input.lower() == 'exit':
            break

        interpretation = ask_gpt3(user_input)
        matched_choice = map_to_choice(interpretation)

        final_response = ""
        if matched_choice:
            print(f"Did you mean you want to \"{matched_choice}\"? (yes/no)")
            confirmation = input().lower()
            if confirmation == "yes":
                final_response = responses.get(matched_choice, "Sorry, I couldn't perform that action.")
                print(final_response)
            else:
                print("I'm sorry for the confusion. Please try again.")
        else:
            print("Sorry, I couldn't understand your request. Please try again.")

        # Save the interaction to the database
        current_data = read_db()
        current_data["interactions"].append({
            "question": user_input,
            "interpretation": interpretation,
            "confirmed_choice": matched_choice,
            "response": final_response
        })
        write_to_db(current_data)

        # Ask if user needs further assistance
        further_assistance = input("Is there anything else I can help you with? (yes/no) ").lower()
        if further_assistance == 'no':
            break

if __name__ == "__main__":
    main()
