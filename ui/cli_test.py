import requests
import json

BASE_URL = "http://127.0.0.1:5000"

def classify_email(subject, body):
    response = requests.post(f"{BASE_URL}/classify", json={"subject": subject, "body": body})
    return response.json()

def provide_feedback(email, correct_category):
    response = requests.post(f"{BASE_URL}/feedback", json={"email": email, "correct_category": correct_category})
    return response.json()

def get_categories():
    response = requests.get(f"{BASE_URL}/categories")
    return response.json()

def add_category(name):
    response = requests.post(f"{BASE_URL}/category", json={"name": name})
    return response.json()

def main():
    print("Available categories:", get_categories())

    subject = input("Enter email subject: ")
    body = input("Enter email body: ")

    classification = classify_email(subject, body)
    print("Classification:", classification)

    correct_category = input("Enter correct category (or leave blank): ")
    if correct_category:
        email = {"subject": subject, "body": body}
        feedback_response = provide_feedback(email, correct_category)
        print("Feedback response:", feedback_response)

    new_category = input("Enter a new category to add (or leave blank): ")
    if new_category:
        add_category_response = add_category(new_category)
        print("Add category response:", add_category_response)
        print("Available categories:", get_categories())

if __name__ == "__main__":
    main()