from flask import Flask, request, jsonify
import categoriser
import logging
from email_generator import EmailGenerator

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Initialize email generator (will use API key from environment)
email_generator = EmailGenerator()

@app.route("/classify", methods=["POST"])
def classify():
    logging.info("Classifying email")
    data = request.get_json()
    if "subject" not in data or "body" not in data:
        return jsonify({"error": "Missing subject or body"}), 400
    subject = data["subject"]
    body = data["body"]
    category, confidence = categoriser.classify_email(subject, body)
    logging.info(f"Classification: {category} with confidence {confidence}")
    return jsonify({"category": category, "confidence": confidence})

@app.route("/feedback", methods=["POST"])
def feedback():
    logging.info("Saving feedback")
    data = request.get_json()
    if "email" not in data or "correct_category" not in data:
        return jsonify({"error": "Missing email or correct_category"}), 400
    email = data["email"]
    correct_category = data["correct_category"]
    categoriser.save_feedback(email, correct_category)
    logging.info("Feedback saved successfully")
    return jsonify({"status": "success"})

@app.route("/categories", methods=["GET"])
def get_categories():
    logging.info("Getting categories")
    categories = categoriser.get_categories()
    logging.info(f"Categories: {categories}")
    return jsonify(categories)

@app.route("/category", methods=["POST"])
def add_category():
    logging.info("Adding category")
    data = request.get_json()
    name = data["name"]
    categoriser.add_category(name)
    logging.info(f"Category {name} added successfully")
    return jsonify({"status": "success"})

@app.route("/generate-emails", methods=["POST"])
def generate_emails():
    """Generate emails for user categorization training"""
    logging.info("Generating emails for training")
    data = request.get_json()
    
    count = data.get("count", 10)
    if count > 50:  # Limit to prevent abuse
        return jsonify({"error": "Maximum 50 emails per request"}), 400
    
    if not email_generator.api_key:
        return jsonify({"error": "No API key configured. Set OPENAI_API_KEY environment variable"}), 500
    
    try:
        user_emails, answer_key = email_generator.generate_for_user_categorization(count=count)
        
        logging.info(f"Generated {len(user_emails)} emails for user training")
        return jsonify({
            "emails": user_emails,
            "answer_key": answer_key,  # Include answer key for validation
            "count": len(user_emails),
            "categories": email_generator.categories,
            "message": f"Generated {len(user_emails)} emails for categorization training"
        })
        
    except Exception as e:
        logging.error(f"Email generation failed: {e}")
        return jsonify({"error": f"Failed to generate emails: {str(e)}"}), 500

@app.route("/validate-categorization", methods=["POST"])
def validate_categorization():
    """Validate user's email categorizations"""
    logging.info("Validating user categorizations")
    data = request.get_json()
    
    user_categorizations = data.get("categorizations", [])
    answer_key = data.get("answer_key", [])
    
    if not user_categorizations:
        return jsonify({"error": "No categorizations provided"}), 400
    
    if not answer_key:
        return jsonify({"error": "No answer key provided"}), 400
    
    # Create lookup for correct answers
    correct_answers = {item["id"]: item["correct_category"] for item in answer_key}
    
    results = []
    correct_count = 0
    
    for categorization in user_categorizations:
        email_id = categorization.get("id")
        user_category = categorization.get("category")
        correct_category = correct_answers.get(email_id)
        
        is_correct = user_category == correct_category
        if is_correct:
            correct_count += 1
            
        results.append({
            "id": email_id,
            "user_category": user_category,
            "correct_category": correct_category,
            "is_correct": is_correct
        })
    
    accuracy = (correct_count / len(results)) * 100 if results else 0
    
    return jsonify({
        "results": results,
        "accuracy": accuracy,
        "correct_count": correct_count,
        "total_count": len(results)
    })

@app.route("/batch-feedback", methods=["POST"])
def batch_feedback():
    """Apply feedback for multiple emails in batch for training"""
    logging.info("Processing batch feedback for training")
    data = request.get_json()
    
    feedback_items = data.get("feedback_items", [])
    if not feedback_items:
        return jsonify({"error": "No feedback items provided"}), 400
    
    successful_feedback = 0
    failed_feedback = 0
    
    for item in feedback_items:
        try:
            email = item.get("email")
            correct_category = item.get("correct_category")
            
            if not email or not correct_category:
                failed_feedback += 1
                continue
            
            categoriser.save_feedback(email, correct_category)
            successful_feedback += 1
            
        except Exception as e:
            logging.error(f"Failed to save feedback item: {e}")
            failed_feedback += 1
    
    logging.info(f"Batch feedback processed: {successful_feedback} successful, {failed_feedback} failed")
    
    return jsonify({
        "status": "completed",
        "successful_feedback": successful_feedback,
        "failed_feedback": failed_feedback,
        "total_processed": len(feedback_items)
    })

@app.route("/training-stats", methods=["GET"])
def get_training_stats():
    """Get training statistics and model performance metrics"""
    logging.info("Getting training statistics")
    
    try:
        # Load feedback data to calculate stats
        with open(FEEDBACK_PATH, "r") as f:
            feedback_data = json.load(f)
        
        total_feedback = len(feedback_data)
        
        # Calculate category distribution in feedback
        category_distribution = {}
        for item in feedback_data:
            category = item.get("correct_category", "Unknown")
            category_distribution[category] = category_distribution.get(category, 0) + 1
        
        # Get available categories
        categories = categoriser.get_categories()
        
        stats = {
            "total_feedback_items": total_feedback,
            "category_distribution": category_distribution,
            "available_categories": categories,
            "total_categories": len(categories)
        }
        
        return jsonify(stats)
        
    except FileNotFoundError:
        return jsonify({
            "total_feedback_items": 0,
            "category_distribution": {},
            "available_categories": categoriser.get_categories(),
            "total_categories": len(categoriser.get_categories())
        })
    except Exception as e:
        logging.error(f"Error getting training stats: {e}")
        return jsonify({"error": f"Failed to get training stats: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=False)