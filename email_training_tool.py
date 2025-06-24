#!/usr/bin/env python3
"""
Email Categorization Training Tool
Uses external LLM API to generate emails for user categorization practice
"""

import json
import requests
import os
from typing import List, Dict
import argparse

class EmailTrainingTool:
    def __init__(self, backend_url: str = "http://localhost:5000"):
        self.backend_url = backend_url
        self.current_emails = []
        self.answer_key = []
        self.categories = []
        
    def generate_emails(self, count: int) -> bool:
        """Generate emails for categorization training"""
        try:
            print(f"Generating {count} emails using external LLM API...")
            response = requests.post(
                f"{self.backend_url}/generate-emails",
                json={"count": count},
                timeout=60  # Longer timeout for LLM API calls
            )
            
            if response.status_code == 200:
                data = response.json()
                self.current_emails = data["emails"]
                self.answer_key = data["answer_key"]
                self.categories = data["categories"]
                print(f"✓ Generated {len(self.current_emails)} emails for training")
                return True
            else:
                error_msg = response.json().get("error", "Unknown error")
                print(f"✗ Failed to generate emails: {error_msg}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Connection error: {e}")
            print("Make sure the backend server is running on http://localhost:5000")
            return False
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    def display_categories(self):
        """Display available categories"""
        print("\nAvailable Categories:")
        for i, category in enumerate(self.categories, 1):
            print(f"  {i:2d}. {category}")
        print()
    
    def categorize_emails_interactive(self):
        """Interactive email categorization"""
        if not self.current_emails:
            print("No emails to categorize. Generate emails first.")
            return
        
        print(f"\n{'='*60}")
        print("EMAIL CATEGORIZATION TRAINING")
        print(f"{'='*60}")
        print(f"You have {len(self.current_emails)} emails to categorize.")
        
        self.display_categories()
        
        user_categorizations = []
        
        for i, email in enumerate(self.current_emails, 1):
            print(f"\n--- EMAIL {i}/{len(self.current_emails)} ---")
            print(f"Subject: {email['subject']}")
            print(f"Body:\n{email['body']}")
            print("-" * 50)
            
            while True:
                try:
                    choice = input(f"Enter category number (1-{len(self.categories)}) or 'q' to quit: ").strip()
                    
                    if choice.lower() == 'q':
                        print("Quitting categorization...")
                        return user_categorizations
                    
                    category_index = int(choice) - 1
                    if 0 <= category_index < len(self.categories):
                        selected_category = self.categories[category_index]
                        user_categorizations.append({
                            "id": email["id"],
                            "category": selected_category
                        })
                        print(f"✓ Categorized as: {selected_category}")
                        break
                    else:
                        print(f"Invalid choice. Please enter a number between 1 and {len(self.categories)}")
                        
                except ValueError:
                    print("Invalid input. Please enter a number or 'q' to quit.")
                except KeyboardInterrupt:
                    print("\nQuitting...")
                    return user_categorizations
        
        return user_categorizations
    
    def validate_categorizations(self, user_categorizations: List[Dict]):
        """Validate user categorizations against correct answers"""
        if not user_categorizations:
            print("No categorizations to validate.")
            return
        
        try:
            response = requests.post(
                f"{self.backend_url}/validate-categorization",
                json={
                    "categorizations": user_categorizations,
                    "answer_key": self.answer_key
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.display_results(data)
            else:
                error_msg = response.json().get("error", "Unknown error")
                print(f"✗ Validation failed: {error_msg}")
                
        except Exception as e:
            print(f"✗ Validation error: {e}")
    
    def display_results(self, validation_data: Dict):
        """Display categorization results"""
        results = validation_data["results"]
        accuracy = validation_data["accuracy"]
        correct_count = validation_data["correct_count"]
        total_count = validation_data["total_count"]
        
        print(f"\n{'='*60}")
        print("CATEGORIZATION RESULTS")
        print(f"{'='*60}")
        print(f"Accuracy: {accuracy:.1f}% ({correct_count}/{total_count})")
        print()
        
        for result in results:
            status = "✓" if result["is_correct"] else "✗"
            print(f"{status} Email {result['id']}: {result['user_category']}")
            if not result["is_correct"]:
                print(f"    Correct answer: {result['correct_category']}")
        
        print(f"\n{'='*60}")
        
        # Provide feedback based on performance
        if accuracy >= 90:
            print("🎉 Excellent work! You have a strong understanding of email categorization.")
        elif accuracy >= 75:
            print("👍 Good job! You're getting the hang of email categorization.")
        elif accuracy >= 60:
            print("📚 Not bad, but there's room for improvement. Keep practicing!")
        else:
            print("💪 Keep practicing! Email categorization takes time to master.")
    
    def save_session(self, filename: str):
        """Save current session to file"""
        session_data = {
            "emails": self.current_emails,
            "answer_key": self.answer_key,
            "categories": self.categories
        }
        
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
        print(f"Session saved to {filename}")
    
    def load_session(self, filename: str):
        """Load session from file"""
        try:
            with open(filename, 'r') as f:
                session_data = json.load(f)
            
            self.current_emails = session_data["emails"]
            self.answer_key = session_data["answer_key"]
            self.categories = session_data["categories"]
            print(f"Session loaded from {filename}")
            return True
        except Exception as e:
            print(f"Failed to load session: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(description="Email Categorization Training Tool")
    parser.add_argument("--count", type=int, default=5, help="Number of emails to generate (default: 5)")
    parser.add_argument("--backend-url", type=str, default="http://localhost:5000", 
                       help="Backend server URL")
    parser.add_argument("--save", type=str, help="Save session to file")
    parser.add_argument("--load", type=str, help="Load session from file")
    parser.add_argument("--generate-only", action="store_true", 
                       help="Only generate emails, don't start interactive categorization")
    
    args = parser.parse_args()
    
    tool = EmailTrainingTool(backend_url=args.backend_url)
    
    # Load existing session if requested
    if args.load:
        if not tool.load_session(args.load):
            return
    else:
        # Generate new emails
        if not tool.generate_emails(args.count):
            print("\nTroubleshooting:")
            print("1. Make sure the backend server is running: python backend/app.py")
            print("2. Set your OpenAI API key: export OPENAI_API_KEY='your-key-here'")
            print("3. Check that you have internet connectivity")
            return
    
    # Save session if requested
    if args.save:
        tool.save_session(args.save)
    
    # Start interactive categorization unless generate-only mode
    if not args.generate_only:
        print("\nStarting interactive categorization...")
        print("Tip: Read each email carefully and consider the business context.")
        
        user_categorizations = tool.categorize_emails_interactive()
        
        if user_categorizations:
            print("\nValidating your categorizations...")
            tool.validate_categorizations(user_categorizations)
        else:
            print("No categorizations to validate.")


if __name__ == "__main__":
    main()