#!/usr/bin/env python3
"""
Demo script for the Automated Training System
Shows how the system uses API calls to train the email categorization model
"""

import time
import requests
from automated_training_system import AutomatedTrainingSystem

def check_backend_status(backend_url="http://localhost:5000"):
    """Check if backend is running and properly configured"""
    print("🔍 Checking backend status...")
    
    try:
        # Test basic connectivity
        response = requests.get(f"{backend_url}/categories", timeout=5)
        if response.status_code != 200:
            print("❌ Backend server not responding properly")
            return False
        
        print("✅ Backend server is running")
        
        # Test email generation capability
        test_response = requests.post(
            f"{backend_url}/generate-emails",
            json={"count": 1},
            timeout=30
        )
        
        if test_response.status_code == 200:
            print("✅ Email generation API is working")
            return True
        else:
            error = test_response.json().get("error", "Unknown error")
            print(f"❌ Email generation failed: {error}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def demo_single_training_cycle():
    """Demonstrate a single training cycle"""
    print("\n" + "="*60)
    print("DEMO: Single Training Cycle")
    print("="*60)
    
    trainer = AutomatedTrainingSystem()
    
    print("This demo will:")
    print("1. 📧 Generate 5 training emails using external LLM API")
    print("2. 🎯 Classify each email using the current model")
    print("3. 📚 Apply feedback for incorrect classifications")
    print("4. 📊 Show accuracy and training results")
    
    input("\nPress Enter to start the demo...")
    
    result = trainer.run_training_cycle(email_count=5)
    
    if result["status"] == "success":
        print("\n✅ Training cycle completed successfully!")
        session_data = result["session_data"]
        training_results = result["training_results"]
        
        print(f"📧 Emails processed: {session_data['email_count']}")
        print(f"🎯 Classifications made: {session_data['classifications_count']}")
        print(f"📊 Accuracy achieved: {training_results['accuracy']:.1f}%")
        print(f"📚 Feedback applied: {training_results['feedback_applied']} corrections")
        print(f"⏱️  Duration: {session_data['duration_seconds']:.1f} seconds")
    else:
        print(f"❌ Training cycle failed: {result.get('reason', 'unknown')}")

def demo_continuous_training():
    """Demonstrate continuous training with multiple cycles"""
    print("\n" + "="*60)
    print("DEMO: Continuous Training")
    print("="*60)
    
    trainer = AutomatedTrainingSystem()
    
    print("This demo will:")
    print("1. 🔄 Run 3 training cycles")
    print("2. 📧 Generate 3 emails per cycle (9 total)")
    print("3. 🎯 Classify and apply feedback for each batch")
    print("4. 📈 Show accuracy improvement over time")
    print("5. ⏳ Wait 10 seconds between cycles")
    
    input("\nPress Enter to start continuous training demo...")
    
    results = trainer.run_continuous_training(
        cycles=3,
        emails_per_cycle=3,
        delay_between_cycles=10
    )
    
    print("\n📊 CONTINUOUS TRAINING RESULTS:")
    print(f"✅ Successful cycles: {results['successful_cycles']}/{results['total_cycles']}")
    print(f"📧 Total emails: {results['total_emails_generated']}")
    print(f"🎯 Total classifications: {results['total_classifications']}")
    print(f"📚 Total feedback applied: {results['total_feedback_applied']}")
    print(f"📊 Average accuracy: {results['average_accuracy']:.1f}%")
    
    if len(results['accuracy_trend']) > 1:
        print(f"📈 Accuracy trend: {results['accuracy_trend'][0]:.1f}% → {results['accuracy_trend'][-1]:.1f}%")

def demo_api_workflow():
    """Demonstrate the individual API calls used in training"""
    print("\n" + "="*60)
    print("DEMO: API Workflow Breakdown")
    print("="*60)
    
    backend_url = "http://localhost:5000"
    
    print("This demo shows the 3 API calls used in automated training:")
    print()
    
    # API Call 1: Generate emails
    print("🔄 API Call 1: Generating emails...")
    try:
        response = requests.post(
            f"{backend_url}/generate-emails",
            json={"count": 2},
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            emails = data["emails"]
            answer_key = data["answer_key"]
            print(f"✅ Generated {len(emails)} emails")
            
            # Show first email
            if emails:
                email = emails[0]
                print(f"   Example: '{email['subject'][:50]}...'")
        else:
            print("❌ Email generation failed")
            return
            
    except Exception as e:
        print(f"❌ API Call 1 failed: {e}")
        return
    
    # API Call 2: Classify emails
    print("\n🔄 API Call 2: Classifying emails...")
    classifications = []
    
    for email in emails:
        try:
            response = requests.post(
                f"{backend_url}/classify",
                json={
                    "subject": email["subject"],
                    "body": email["body"]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                classifications.append({
                    "email_id": email["id"],
                    "predicted": result["category"],
                    "confidence": result["confidence"],
                    "email": email
                })
                
        except Exception as e:
            print(f"❌ Classification failed for email {email['id']}: {e}")
    
    print(f"✅ Classified {len(classifications)} emails")
    
    # API Call 3: Apply feedback
    print("\n🔄 API Call 3: Applying feedback...")
    correct_answers = {item["id"]: item["correct_category"] for item in answer_key}
    feedback_applied = 0
    
    for classification in classifications:
        email_id = classification["email_id"]
        predicted = classification["predicted"]
        correct = correct_answers.get(email_id)
        
        print(f"   Email {email_id}: {predicted} {'✅' if predicted == correct else '❌ → ' + correct}")
        
        if predicted != correct:
            try:
                response = requests.post(
                    f"{backend_url}/feedback",
                    json={
                        "email": {
                            "subject": classification["email"]["subject"],
                            "body": classification["email"]["body"]
                        },
                        "correct_category": correct
                    },
                    timeout=10
                )
                
                if response.status_code == 200:
                    feedback_applied += 1
                    
            except Exception as e:
                print(f"❌ Feedback failed for email {email_id}: {e}")
    
    print(f"✅ Applied {feedback_applied} feedback corrections")

def main():
    print("🤖 Automated Training System Demo")
    print("="*60)
    
    # Check backend status first
    if not check_backend_status():
        print("\n❌ Backend not ready. Please ensure:")
        print("1. Backend server is running: python backend/app.py")
        print("2. OpenAI API key is set: export OPENAI_API_KEY='your-key'")
        print("3. Internet connectivity is available")
        return
    
    print("\n🎯 Choose a demo:")
    print("1. Single Training Cycle (5 emails)")
    print("2. Continuous Training (3 cycles)")
    print("3. API Workflow Breakdown (2 emails)")
    print("4. Run all demos")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        demo_single_training_cycle()
    elif choice == "2":
        demo_continuous_training()
    elif choice == "3":
        demo_api_workflow()
    elif choice == "4":
        print("\n🚀 Running all demos...")
        demo_api_workflow()
        demo_single_training_cycle()
        demo_continuous_training()
    else:
        print("❌ Invalid choice. Please run the script again.")
        return
    
    print("\n✅ Demo completed!")
    print("\nTo run your own automated training:")
    print("python automated_training_system.py --cycles 5 --emails-per-cycle 10")

if __name__ == "__main__":
    main()