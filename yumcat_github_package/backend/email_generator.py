"""
Email Generator using External LLM API
Generates realistic emails for user categorization training
"""

import openai
import json
import random
from typing import List, Dict, Any, Optional
import os
from datetime import datetime, timedelta
import requests
import logging

class EmailGenerator:
    def __init__(self, api_key: str = None, model: str = "gpt-3.5-turbo", provider: str = "openai"):
        """
        Initialize the email generator with API credentials
        
        Args:
            api_key: API key for the LLM service
            model: Model to use (gpt-3.5-turbo, gpt-4, etc.)
            provider: LLM provider (openai, anthropic, etc.)
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.provider = provider
        
        if self.provider == "openai" and self.api_key:
            openai.api_key = self.api_key
        
        # Load categories from the existing categories.json
        self.categories = self._load_categories()
    
    def _load_categories(self) -> List[str]:
        """Load email categories from the categories.json file"""
        try:
            with open('backend/data/categories.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.warning("Categories file not found, using fallback categories")
            return [
                "Complaint - Product/Service",
                "Sales Opportunity - New Business",
                "Action Required - Urgent Response",
                "Legal Escalation - Threat/Litigation",
                "Good News - Customer Success",
                "Technical Support - Bug Report",
                "General Inquiry"
            ]
    
    def generate_email_prompt(self, category: str, difficulty: str = "medium") -> str:
        """
        Create a prompt for generating realistic business emails
        
        Args:
            category: The email category to generate
            difficulty: Difficulty level (easy, medium, hard)
        """
        difficulty_instructions = {
            "easy": "Make this email very clearly and obviously belong to this category with explicit keywords and phrases.",
            "medium": "Make this email moderately clear but with some subtlety that requires understanding context.",
            "hard": "Make this email subtle and borderline - it could potentially fit multiple categories but should still primarily belong to the specified one."
        }
        
        business_contexts = [
            "software company", "manufacturing business", "consulting firm", 
            "retail store", "healthcare provider", "financial services",
            "e-commerce platform", "marketing agency", "law firm", "restaurant"
        ]
        
        sender_types = [
            "frustrated customer", "potential client", "existing customer",
            "business partner", "vendor", "employee", "journalist",
            "legal representative", "government official", "competitor"
        ]
        
        context = random.choice(business_contexts)
        sender = random.choice(sender_types)
        
        prompt = f"""Generate a realistic business email that belongs to the category: "{category}"

Context: This email is being sent to a {context} from a {sender}.

Requirements:
1. {difficulty_instructions.get(difficulty, difficulty_instructions['medium'])}
2. Include both a subject line and email body
3. Make it sound natural and realistic
4. Use appropriate business tone and language
5. Include specific details that make it believable
6. The email should be 2-4 paragraphs long
7. Don't explicitly mention the category name in the email

Format your response as JSON:
{{
    "subject": "Email subject line here",
    "body": "Email body content here"
}}

Generate the email now:"""
        
        return prompt
    
    def generate_single_email(self, category: str, difficulty: str = "medium") -> Optional[Dict[str, str]]:
        """
        Generate a single email for the specified category
        
        Args:
            category: Email category to generate
            difficulty: Difficulty level (easy, medium, hard)
            
        Returns:
            Dictionary with subject, body, category, and metadata
        """
        if category not in self.categories:
            logging.error(f"Category '{category}' not found in available categories")
            return None
        
        prompt = self.generate_email_prompt(category, difficulty)
        
        try:
            if self.provider == "openai":
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "You are an expert at generating realistic business emails for training purposes."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
                    max_tokens=500
                )
                
                content = response.choices[0].message.content.strip()
                
                # Parse JSON response
                try:
                    email_data = json.loads(content)
                    return {
                        "subject": email_data["subject"],
                        "body": email_data["body"],
                        "category": category,
                        "difficulty": difficulty,
                        "generated_at": datetime.now().isoformat(),
                        "model": self.model
                    }
                except json.JSONDecodeError:
                    logging.error(f"Failed to parse LLM response as JSON: {content}")
                    return None
                    
            else:
                logging.error(f"Provider '{self.provider}' not implemented yet")
                return None
                
        except Exception as e:
            logging.error(f"Failed to generate email: {e}")
            return None
    
    def generate_emails_batch(self, count: int, categories: List[str] = None, 
                            difficulty_distribution: Dict[str, float] = None) -> List[Dict[str, str]]:
        """
        Generate a batch of emails across categories
        
        Args:
            count: Total number of emails to generate
            categories: List of categories to use (defaults to all)
            difficulty_distribution: Distribution of difficulties {"easy": 0.3, "medium": 0.5, "hard": 0.2}
            
        Returns:
            List of generated email dictionaries
        """
        if categories is None:
            categories = self.categories
        
        if difficulty_distribution is None:
            difficulty_distribution = {"easy": 0.3, "medium": 0.5, "hard": 0.2}
        
        emails = []
        categories_cycle = categories * (count // len(categories) + 1)
        
        for i in range(count):
            category = categories_cycle[i]
            
            # Determine difficulty based on distribution
            rand = random.random()
            cumulative = 0
            difficulty = "medium"  # default
            
            for diff, prob in difficulty_distribution.items():
                cumulative += prob
                if rand <= cumulative:
                    difficulty = diff
                    break
            
            email = self.generate_single_email(category, difficulty)
            if email:
                emails.append(email)
            else:
                logging.warning(f"Failed to generate email for category: {category}")
        
        return emails
    
    def generate_for_user_categorization(self, count: int, save_to_file: str = None) -> List[Dict[str, str]]:
        """
        Generate emails specifically for user categorization training
        
        Args:
            count: Number of emails to generate
            save_to_file: Optional file path to save the emails
            
        Returns:
            List of emails without category labels (for user to categorize)
        """
        # Generate emails with varied difficulty
        emails = self.generate_emails_batch(
            count=count,
            difficulty_distribution={"easy": 0.2, "medium": 0.6, "hard": 0.2}
        )
        
        # Remove category information for user training
        user_emails = []
        answer_key = []
        
        for i, email in enumerate(emails):
            user_email = {
                "id": i + 1,
                "subject": email["subject"],
                "body": email["body"],
                "user_category": "",  # To be filled by user
                "generated_at": email["generated_at"]
            }
            user_emails.append(user_email)
            
            # Keep answer key separate
            answer_key.append({
                "id": i + 1,
                "correct_category": email["category"],
                "difficulty": email["difficulty"]
            })
        
        # Save to files if requested
        if save_to_file:
            # Save user emails (without answers)
            with open(save_to_file, 'w') as f:
                json.dump(user_emails, f, indent=2)
            
            # Save answer key separately
            answer_file = save_to_file.replace('.json', '_answers.json')
            with open(answer_file, 'w') as f:
                json.dump(answer_key, f, indent=2)
            
            logging.info(f"Saved {len(user_emails)} emails to {save_to_file}")
            logging.info(f"Saved answer key to {answer_file}")
        
        return user_emails, answer_key


def main():
    """CLI interface for email generation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate emails using external LLM API")
    parser.add_argument("--count", type=int, default=10, help="Number of emails to generate")
    parser.add_argument("--api-key", type=str, help="OpenAI API key (or set OPENAI_API_KEY env var)")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="LLM model to use")
    parser.add_argument("--category", type=str, help="Generate emails for specific category only")
    parser.add_argument("--difficulty", type=str, choices=["easy", "medium", "hard"], 
                       default="medium", help="Difficulty level")
    parser.add_argument("--output", type=str, help="Save emails to JSON file")
    parser.add_argument("--for-training", action="store_true", 
                       help="Generate emails for user categorization training (removes category labels)")
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = EmailGenerator(api_key=args.api_key, model=args.model)
    
    if not generator.api_key:
        print("Error: No API key provided. Set OPENAI_API_KEY environment variable or use --api-key")
        return
    
    print(f"Generating {args.count} emails using {args.model}...")
    
    if args.for_training:
        # Generate for user training
        user_emails, answer_key = generator.generate_for_user_categorization(
            count=args.count,
            save_to_file=args.output
        )
        
        print(f"\nGenerated {len(user_emails)} emails for user categorization training")
        print("Categories available for classification:")
        for i, cat in enumerate(generator.categories, 1):
            print(f"  {i}. {cat}")
        
        if not args.output:
            print("\nFirst 3 emails for preview:")
            for email in user_emails[:3]:
                print(f"\n--- Email {email['id']} ---")
                print(f"Subject: {email['subject']}")
                print(f"Body: {email['body'][:200]}...")
                print("Your category: _______________")
    
    elif args.category:
        # Generate for specific category
        if args.category not in generator.categories:
            print(f"Error: Category '{args.category}' not found.")
            print("Available categories:")
            for cat in generator.categories:
                print(f"  - {cat}")
            return
        
        emails = []
        for i in range(args.count):
            email = generator.generate_single_email(args.category, args.difficulty)
            if email:
                emails.append(email)
        
        print(f"\nGenerated {len(emails)} emails for category: {args.category}")
        
        for email in emails:
            print(f"\n--- {email['difficulty'].upper()} DIFFICULTY ---")
            print(f"Subject: {email['subject']}")
            print(f"Body: {email['body']}")
    
    else:
        # Generate across all categories
        emails = generator.generate_emails_batch(count=args.count)
        
        print(f"\nGenerated {len(emails)} emails across {len(generator.categories)} categories")
        
        # Show distribution
        category_counts = {}
        for email in emails:
            cat = email['category']
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        print("\nCategory distribution:")
        for cat, count in category_counts.items():
            print(f"  {cat}: {count}")
    
    # Save to file if requested
    if args.output and not args.for_training:
        with open(args.output, 'w') as f:
            json.dump(emails, f, indent=2)
        print(f"\nSaved to {args.output}")


if __name__ == "__main__":
    main()