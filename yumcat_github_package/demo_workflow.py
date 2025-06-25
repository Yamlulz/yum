#!/usr/bin/env python3
"""
Complete Demo Workflow for YUM Email Categorizer

This script demonstrates the full workflow:
1. Generate training emails for different categories
2. Test LLM classification
3. Show accuracy metrics
4. Demonstrate feedback loop
"""

import json
import requests
import time
import sys
from generate_training_emails import generate_training_email, TRAINING_TEMPLATES

def check_api_status():
    """Check if the Flask API is running"""
    try:
        response = requests.get("http://127.0.0.1:5000/categories", timeout=5)
        return response.status_code == 200
    except:
        return False

def check_llm_status():
    """Check if Ollama LLM is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False

def classify_email(subject, body):
    """Classify an email using the API"""
    try:
        response = requests.post(
            "http://127.0.0.1:5000/classify",
            json={"subject": subject, "body": body},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Classification error: {e}")
    return None

def submit_feedback(email, correct_category):
    """Submit feedback to improve the model"""
    try:
        response = requests.post(
            "http://127.0.0.1:5000/feedback",
            json={"email": email, "correct_category": correct_category},
            timeout=5
        )
        return response.status_code == 200
    except:
        return False

def demo_category_classification(category, num_emails=3):
    """Demo classification for a specific category"""
    print(f"\n🔍 Testing Category: {category}")
    print("=" * 60)
    
    correct_predictions = 0
    total_predictions = 0
    
    for match_type in ["exact", "partial"]:
        print(f"\n📧 {match_type.upper()} MATCH EXAMPLES:")
        
        for i in range(num_emails):
            email = generate_training_email(category, match_type)
            if not email:
                continue
                
            print(f"\n--- Email {i+1} ({match_type}) ---")
            print(f"Subject: {email['subject']}")
            print(f"Body: {email['body'][:100]}...")
            
            # Classify the email
            result = classify_email(email['subject'], email['body'])
            if result:
                predicted = result.get('category')
                confidence = result.get('confidence', 0)
                correct = predicted == category
                
                status = "✅ CORRECT" if correct else "❌ INCORRECT"
                print(f"Expected: {category}")
                print(f"Predicted: {predicted} (confidence: {confidence:.2f}) {status}")
                
                total_predictions += 1
                if correct:
                    correct_predictions += 1
                else:
                    # Submit feedback for incorrect predictions
                    feedback_success = submit_feedback(
                        {"subject": email['subject'], "body": email['body']},
                        category
                    )
                    if feedback_success:
                        print("📝 Feedback submitted for model improvement")
            else:
                print("❌ Classification failed")
            
            time.sleep(1)  # Rate limiting
    
    if total_predictions > 0:
        accuracy = (correct_predictions / total_predictions) * 100
        print(f"\n📊 Category Accuracy: {accuracy:.1f}% ({correct_predictions}/{total_predictions})")
    
    return correct_predictions, total_predictions

def main():
    """Main demo workflow"""
    print("🤖 YUM Email Categorizer - Complete Demo Workflow")
    print("=" * 60)
    
    # Check system status
    print("\n🔧 System Status Check:")
    api_running = check_api_status()
    llm_running = check_llm_status()
    
    print(f"Flask API: {'✅ Running' if api_running else '❌ Not running'}")
    print(f"Ollama LLM: {'✅ Running' if llm_running else '❌ Not running'}")
    
    if not api_running:
        print("\n❌ Flask API is not running. Please start it with:")
        print("python backend/app.py")
        sys.exit(1)
    
    if not llm_running:
        print("\n⚠️  Ollama LLM is not running. Classification will use fallback logic.")
        print("To start Ollama: ollama serve")
        print("To install: ./setup_local_llm.sh")
    
    # Get available categories
    try:
        response = requests.get("http://127.0.0.1:5000/categories")
        categories = response.json()
        print(f"\n📋 Available Categories: {len(categories)}")
    except:
        print("❌ Failed to get categories")
        sys.exit(1)
    
    # Demo key business categories
    demo_categories = [
        "Complaint - Product/Service",
        "Sales Opportunity - New Business", 
        "Action Required - Urgent Response",
        "Legal Escalation - Threat/Litigation",
        "Good News - Customer Success",
        "Crisis Management - Security Incident"
    ]
    
    total_correct = 0
    total_tested = 0
    
    print(f"\n🎯 Testing {len(demo_categories)} Key Business Categories")
    print("This will generate realistic emails and test classification accuracy...")
    
    for category in demo_categories:
        if category in categories:
            correct, tested = demo_category_classification(category, num_emails=2)
            total_correct += correct
            total_tested += tested
        else:
            print(f"⚠️  Category not found: {category}")
    
    # Overall results
    print(f"\n🏆 OVERALL RESULTS")
    print("=" * 60)
    if total_tested > 0:
        overall_accuracy = (total_correct / total_tested) * 100
        print(f"Total Emails Tested: {total_tested}")
        print(f"Correct Classifications: {total_correct}")
        print(f"Overall Accuracy: {overall_accuracy:.1f}%")
        
        if overall_accuracy >= 80:
            print("🎉 Excellent! The system is performing very well.")
        elif overall_accuracy >= 60:
            print("👍 Good performance. Consider fine-tuning with more training data.")
        else:
            print("⚠️  Performance needs improvement. Check LLM setup and training data.")
    
    # Demo feedback loop
    print(f"\n🔄 Feedback Loop Demo")
    print("=" * 30)
    
    # Create a test email that might be misclassified
    test_email = {
        "subject": "Partnership Opportunity - Legal Review Needed",
        "body": "We're interested in a strategic partnership but need our legal team to review the contract terms first. This could be a great opportunity but we want to ensure compliance."
    }
    
    print("📧 Test Email (Ambiguous Category):")
    print(f"Subject: {test_email['subject']}")
    print(f"Body: {test_email['body']}")
    
    result = classify_email(test_email['subject'], test_email['body'])
    if result:
        print(f"\n🤖 AI Prediction: {result['category']} (confidence: {result['confidence']:.2f})")
        print("💭 This email could be classified as:")
        print("   - Sales Opportunity - Partnership")
        print("   - Legal Escalation - Compliance Issue")
        print("   - Action Required - Documentation")
        
        # Simulate user feedback
        correct_category = "Sales Opportunity - Partnership"
        feedback_success = submit_feedback(test_email, correct_category)
        if feedback_success:
            print(f"✅ User feedback submitted: Correct category is '{correct_category}'")
            print("📈 This feedback will help improve future classifications")
    
    print(f"\n✨ Demo Complete!")
    print("=" * 60)
    print("🔧 Next Steps:")
    print("1. Review classification accuracy for your specific use cases")
    print("2. Generate more training data: python generate_training_emails.py")
    print("3. Submit feedback for misclassified emails to improve accuracy")
    print("4. Integrate with Outlook using the Office.js add-in (coming soon)")
    print("\n💡 Tips:")
    print("- Higher confidence scores (>0.8) indicate more reliable classifications")
    print("- Submit feedback for edge cases to improve model performance")
    print("- Monitor accuracy over time as the system learns from feedback")

if __name__ == "__main__":
    main()