import json
import random
import hashlib
import requests
import logging

CATEGORIES_PATH = "backend/data/categories.json"
FEEDBACK_PATH = "backend/data/feedback.json"

def get_categories():
    with open(CATEGORIES_PATH, "r") as f:
        return json.load(f)

def add_category(name):
    categories = get_categories()
    categories.append(name)
    with open(CATEGORIES_PATH, "w") as f:
        json.dump(categories, f, indent=2)

def save_feedback(email, correct_category):
    with open(FEEDBACK_PATH, "r+") as f:
        try:
            feedback = json.load(f)
        except json.JSONDecodeError:
            feedback = []
        except Exception as e:
            print(f"Error loading feedback: {e}")
            feedback = []

        # Hash the email content for security
        email_string = json.dumps(email, sort_keys=True).encode('utf-8')
        email_hash = hashlib.sha256(email_string).hexdigest()

        feedback.append({"email_hash": email_hash, "correct_category": correct_category})
        f.seek(0)
        json.dump(feedback, f, indent=2)

def classify_email(subject, body):
    """
    Classify email using local LLM (Ollama or similar)
    Falls back to dummy logic if LLM is unavailable
    """
    categories = get_categories()
    
    try:
        # Try to use local LLM first
        category, confidence = classify_with_llm(subject, body, categories)
        return category, confidence
    except Exception as e:
        logging.warning(f"LLM classification failed: {e}. Using fallback logic.")
        # Fallback to simple logic if LLM unavailable
        return classify_fallback(subject, body, categories)

def classify_with_llm(subject, body, categories):
    """
    Use local LLM (Ollama) for email classification
    """
    # Construct prompt for LLM
    categories_list = "\n".join([f"- {cat}" for cat in categories])
    
    prompt = f"""You are an expert email classifier for business communications.

Analyze this email and classify it into ONE of the following categories:

{categories_list}

Email Subject: {subject}
Email Body: {body}

Instructions:
1. Choose the MOST APPROPRIATE category from the list above
2. Consider business context, urgency, and potential impact
3. Look for keywords that indicate complaints, opportunities, legal issues, etc.
4. Respond with ONLY the category name, exactly as listed above

Category:"""

    # Try Ollama API (default local LLM setup)
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",  # Lightweight model for fast classification
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,  # Low temperature for consistent classification
                    "top_p": 0.9,
                    "max_tokens": 50
                }
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            predicted_category = result.get("response", "").strip()
            
            # Validate that the predicted category is in our list
            if predicted_category in categories:
                return predicted_category, 0.85
            else:
                # Try to find closest match
                for cat in categories:
                    if predicted_category.lower() in cat.lower() or cat.lower() in predicted_category.lower():
                        return cat, 0.75
                
                # If no match found, use fallback
                logging.warning(f"LLM returned invalid category: {predicted_category}")
                return classify_fallback(subject, body, categories)
        
    except requests.exceptions.RequestException as e:
        logging.warning(f"Ollama API request failed: {e}")
        raise e
    
    # If we get here, something went wrong
    raise Exception("LLM classification failed")

def classify_fallback(subject, body, categories):
    """
    Fallback classification logic when LLM is unavailable
    Uses simple keyword matching
    """
    text = (subject + " " + body).lower()
    
    # Simple keyword-based classification
    keyword_mapping = {
        "complaint": ["complaint", "problem", "issue", "broken", "defective", "poor", "terrible", "awful", "disappointed"],
        "sales": ["quote", "pricing", "proposal", "interested", "buy", "purchase", "upgrade", "partnership"],
        "urgent": ["urgent", "asap", "immediate", "emergency", "critical", "time sensitive"],
        "legal": ["legal", "lawsuit", "attorney", "lawyer", "contract", "breach", "violation", "sue"],
        "good news": ["success", "award", "recognition", "excellent", "outstanding", "fantastic", "impressed"],
        "technical": ["bug", "error", "technical", "support", "help", "not working", "malfunction"]
    }
    
    # Check for keyword matches
    for category_type, keywords in keyword_mapping.items():
        if any(keyword in text for keyword in keywords):
            # Find matching category from our list
            for cat in categories:
                if category_type.replace(" ", "").lower() in cat.lower().replace(" ", "").replace("-", ""):
                    return cat, 0.6
    
    # Default to General Inquiry
    general_categories = [cat for cat in categories if "general" in cat.lower() or "inquiry" in cat.lower()]
    if general_categories:
        return general_categories[0], 0.3
    
    # If no general category, return first category
    return categories[0] if categories else "Unknown", 0.2