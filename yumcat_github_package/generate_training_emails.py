#!/usr/bin/env python3
"""
Training Email Generator for Business Email Categorization

Generates realistic training emails for each business category with varying levels of exactness:
- Exact matches: Clear, unambiguous examples
- Partial matches: More subtle or mixed signals
- Edge cases: Borderline examples that test classification boundaries
"""

import json
import random
import requests
from datetime import datetime, timedelta

# Training email templates for each category
TRAINING_TEMPLATES = {
    "Complaint - Product/Service": {
        "exact": [
            {
                "subject": "Defective Product - Immediate Replacement Required",
                "body": "I purchased your product last week and it's completely broken. The quality is terrible and I'm extremely disappointed. This is unacceptable and I demand a full refund or replacement immediately."
            },
            {
                "subject": "Poor Service Quality - Very Unsatisfied Customer",
                "body": "Your service has been awful. The product doesn't work as advertised and I feel like I've wasted my money. This is the worst experience I've had with any company."
            }
        ],
        "partial": [
            {
                "subject": "Issues with Recent Purchase",
                "body": "Hi, I'm having some problems with the item I bought. It's not quite what I expected and I'm wondering if there's anything that can be done about it."
            },
            {
                "subject": "Product Not Meeting Expectations",
                "body": "The product arrived but it's not performing as well as I hoped. Could we discuss some options for resolving this?"
            }
        ]
    },
    
    "Complaint - Billing/Payment": {
        "exact": [
            {
                "subject": "BILLING ERROR - Overcharged on Invoice #12345",
                "body": "I've been overcharged $500 on my latest invoice. This is a clear billing error and I need this corrected immediately. I should not have to pay for charges I didn't incur."
            },
            {
                "subject": "Refund Request - Wrong Amount Charged",
                "body": "You charged my credit card the wrong amount. I was supposed to be charged $100 but you took $200. I need this billing dispute resolved and the difference refunded."
            }
        ],
        "partial": [
            {
                "subject": "Question About Recent Charge",
                "body": "I noticed a charge on my account that seems higher than expected. Could you help me understand what this covers?"
            }
        ]
    },
    
    "Sales Opportunity - New Business": {
        "exact": [
            {
                "subject": "Request for Quote - New Project Opportunity",
                "body": "We're looking to implement a new system and are interested in your services. Could you provide a detailed quote for a project involving 500 users? We have budget approved and are ready to move forward."
            },
            {
                "subject": "Interested in Your Services - Large Contract Potential",
                "body": "Our company is expanding and we need a reliable partner. We're looking at a multi-year contract worth approximately $2M. Can we schedule a meeting to discuss our requirements?"
            }
        ],
        "partial": [
            {
                "subject": "Information Request",
                "body": "Hi, I came across your website and I'm curious about your pricing. Could you send me some basic information about your services?"
            },
            {
                "subject": "Demo Request",
                "body": "We might be interested in your solution. Would it be possible to see a demo sometime next week?"
            }
        ]
    },
    
    "Action Required - Urgent Response": {
        "exact": [
            {
                "subject": "URGENT: System Critical Error - Immediate Action Required",
                "body": "CRITICAL ALERT: Our production system is down and affecting all customers. We need immediate assistance to resolve this emergency situation. Please respond ASAP."
            },
            {
                "subject": "EMERGENCY: Security Breach Detected - Act Now",
                "body": "We've detected unauthorized access to our systems. This is a time-sensitive security emergency that requires immediate attention and response."
            }
        ],
        "partial": [
            {
                "subject": "Quick Response Needed",
                "body": "Hi, we have a situation that needs attention fairly soon. Could you get back to me when you have a chance today?"
            }
        ]
    },
    
    "Legal Escalation - Threat/Litigation": {
        "exact": [
            {
                "subject": "Legal Notice - Breach of Contract",
                "body": "This is formal notice that your company is in breach of our contract dated January 15, 2024. If this matter is not resolved within 30 days, we will have no choice but to pursue legal action including filing a lawsuit."
            },
            {
                "subject": "Attorney Communication - Litigation Threat",
                "body": "I am writing on behalf of my client regarding the ongoing dispute. Unless we receive a satisfactory response within 10 business days, we will proceed with filing a lawsuit in federal court."
            }
        ],
        "partial": [
            {
                "subject": "Contract Concerns",
                "body": "We have some concerns about the contract terms and how they're being implemented. We'd like to discuss this before it becomes a bigger issue."
            }
        ]
    },
    
    "Reputational Risk - Media Inquiry": {
        "exact": [
            {
                "subject": "Media Inquiry - Journalist Seeking Comment",
                "body": "I'm a reporter with TechNews Daily working on a story about data security practices. I'd like to get your company's comment on recent allegations. My deadline is tomorrow at 5 PM."
            },
            {
                "subject": "Press Inquiry - Need Response for Article",
                "body": "I'm writing an article about your industry and would like to include your perspective. This will be published in a major business publication next week."
            }
        ],
        "partial": [
            {
                "subject": "Research Request",
                "body": "I'm working on a project about companies in your sector. Would someone be available for a brief interview?"
            }
        ]
    },
    
    "Good News - Customer Success": {
        "exact": [
            {
                "subject": "Amazing Results - Exceeded All Expectations!",
                "body": "I wanted to share our incredible success story. Since implementing your solution, we've seen a 300% increase in efficiency and saved over $1M annually. This has been a fantastic outcome that exceeded all our expectations."
            },
            {
                "subject": "Outstanding Success - Thank You!",
                "body": "Your team delivered outstanding results on our project. The implementation was flawless and the results have been amazing. We're seeing incredible improvements across all metrics."
            }
        ],
        "partial": [
            {
                "subject": "Positive Update",
                "body": "Things are going well with the new system. We're seeing some good improvements and the team is happy with the results so far."
            }
        ]
    },
    
    "Crisis Management - Security Incident": {
        "exact": [
            {
                "subject": "SECURITY BREACH ALERT - Immediate Response Required",
                "body": "We've detected a security breach in our systems. Unauthorized access has been identified and we need immediate assistance to contain the incident and assess the damage. This is a critical security emergency."
            },
            {
                "subject": "Data Compromise Incident - Urgent Action Needed",
                "body": "Our security team has identified a potential data breach affecting customer information. We need to activate our incident response plan immediately and notify all stakeholders."
            }
        ],
        "partial": [
            {
                "subject": "Security Concern",
                "body": "We've noticed some unusual activity in our logs that might be worth investigating. Could your security team take a look when they have time?"
            }
        ]
    },
    
    "Executive Attention - VIP Customer": {
        "exact": [
            {
                "subject": "VIP Client Issue - CEO Attention Required",
                "body": "Our largest client, GlobalCorp (worth $50M annually), is experiencing issues and their CEO has personally called our CEO. This needs immediate executive attention and resolution."
            },
            {
                "subject": "Key Account Alert - Major Customer Concern",
                "body": "This is regarding our top-tier client who represents 30% of our revenue. They have escalated an issue to the C-level and we need senior leadership involvement immediately."
            }
        ],
        "partial": [
            {
                "subject": "Important Client Update",
                "body": "One of our key clients has some concerns they'd like to discuss. They've asked if someone from senior management could reach out."
            }
        ]
    },
    
    "Financial - Payment Overdue": {
        "exact": [
            {
                "subject": "OVERDUE PAYMENT NOTICE - 60 Days Past Due",
                "body": "Your account is now 60 days past due with an outstanding balance of $25,000. Immediate payment is required to avoid further collection action and potential service suspension."
            },
            {
                "subject": "Final Notice - Payment Required Immediately",
                "body": "This is your final notice for the overdue payment of $15,000. If payment is not received within 5 business days, we will be forced to take collection action."
            }
        ],
        "partial": [
            {
                "subject": "Payment Reminder",
                "body": "Just a friendly reminder that we haven't received payment for invoice #12345 yet. Could you let us know when we might expect payment?"
            }
        ]
    },
    
    "Technical Support - Bug Report": {
        "exact": [
            {
                "subject": "Critical Bug Report - System Malfunction",
                "body": "We've discovered a critical bug in the software that's causing data corruption. This is a serious technical issue that needs immediate attention from your development team."
            },
            {
                "subject": "Software Error - Production Issue",
                "body": "The application is throwing errors in production and users can't complete their work. This bug is affecting our entire operation and needs urgent technical support."
            }
        ],
        "partial": [
            {
                "subject": "Technical Question",
                "body": "We're having some trouble with one of the features. It's not working quite as expected. Could someone from technical support help us figure this out?"
            }
        ]
    },
    
    "Customer Retention - Churn Risk": {
        "exact": [
            {
                "subject": "Cancellation Notice - Switching to Competitor",
                "body": "We've decided to cancel our service and switch to CompetitorCorp. Their pricing is better and they offer features we need. Please process our cancellation effective next month."
            },
            {
                "subject": "Service Termination Request",
                "body": "We're not satisfied with the service and have found a better alternative. Please terminate our contract and provide final billing information."
            }
        ],
        "partial": [
            {
                "subject": "Exploring Options",
                "body": "We're reviewing our current services and looking at different options in the market. Could we discuss our current plan and what alternatives might be available?"
            }
        ]
    },
    
    "General Inquiry": {
        "exact": [
            {
                "subject": "General Question About Services",
                "body": "Hi, I have a general question about your services. Could someone provide me with some basic information about what you offer?"
            },
            {
                "subject": "Information Request",
                "body": "I'm researching different options and would like to learn more about your company. Could you send me some general information?"
            }
        ],
        "partial": [
            {
                "subject": "Quick Question",
                "body": "I have a quick question about your business hours. What time do you close on Fridays?"
            }
        ]
    }
}

def generate_training_email(category, match_type="exact"):
    """Generate a training email for a specific category and match type"""
    if category not in TRAINING_TEMPLATES:
        return None
    
    if match_type not in TRAINING_TEMPLATES[category]:
        match_type = "exact"  # fallback
    
    templates = TRAINING_TEMPLATES[category][match_type]
    if not templates:
        return None
    
    template = random.choice(templates)
    
    # Add some variation to make emails more realistic
    variations = {
        "urgent_prefixes": ["URGENT: ", "IMMEDIATE: ", "CRITICAL: ", ""],
        "polite_endings": [
            "\n\nBest regards,\nJohn Smith",
            "\n\nThank you,\nSarah Johnson", 
            "\n\nSincerely,\nMike Davis",
            "\n\nKind regards,\nEmily Wilson",
            ""
        ],
        "company_names": ["ABC Corp", "TechStart Inc", "Global Solutions", "Innovation Labs", ""],
        "reference_numbers": ["#12345", "#REF-2024-001", "#TKT-789", ""]
    }
    
    subject = template["subject"]
    body = template["body"]
    
    # Add random variations
    if random.random() < 0.3:  # 30% chance to add urgent prefix
        subject = random.choice(variations["urgent_prefixes"]) + subject
    
    if random.random() < 0.7:  # 70% chance to add polite ending
        body += random.choice(variations["polite_endings"])
    
    if random.random() < 0.4:  # 40% chance to add company reference
        company = random.choice(variations["company_names"])
        if company:
            body = f"From: {company}\n\n" + body
    
    if random.random() < 0.3:  # 30% chance to add reference number
        ref = random.choice(variations["reference_numbers"])
        if ref:
            subject += f" {ref}"
    
    return {
        "subject": subject,
        "body": body,
        "category": category,
        "match_type": match_type
    }

def generate_training_dataset(emails_per_category=10, exact_ratio=0.7):
    """
    Generate a complete training dataset
    
    Args:
        emails_per_category: Number of emails to generate per category
        exact_ratio: Ratio of exact matches vs partial matches (0.7 = 70% exact, 30% partial)
    """
    dataset = []
    categories = list(TRAINING_TEMPLATES.keys())
    
    for category in categories:
        for i in range(emails_per_category):
            # Determine match type based on ratio
            match_type = "exact" if random.random() < exact_ratio else "partial"
            
            email = generate_training_email(category, match_type)
            if email:
                dataset.append(email)
    
    return dataset

def test_classification_api(email_data, api_url="http://127.0.0.1:5000/classify"):
    """Test the classification API with generated email"""
    try:
        response = requests.post(api_url, json={
            "subject": email_data["subject"],
            "body": email_data["body"]
        })
        
        if response.status_code == 200:
            result = response.json()
            return {
                "predicted": result.get("category"),
                "confidence": result.get("confidence"),
                "actual": email_data["category"],
                "match_type": email_data["match_type"],
                "correct": result.get("category") == email_data["category"]
            }
    except Exception as e:
        print(f"API test failed: {e}")
    
    return None

def main():
    """Main function to generate and test training emails"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate training emails for email categorization")
    parser.add_argument("--count", type=int, default=5, help="Emails per category")
    parser.add_argument("--exact-ratio", type=float, default=0.7, help="Ratio of exact matches")
    parser.add_argument("--test-api", action="store_true", help="Test generated emails against API")
    parser.add_argument("--output", type=str, help="Save dataset to JSON file")
    parser.add_argument("--category", type=str, help="Generate emails for specific category only")
    
    args = parser.parse_args()
    
    if args.category:
        # Generate emails for specific category
        if args.category in TRAINING_TEMPLATES:
            emails = []
            for i in range(args.count):
                match_type = "exact" if random.random() < args.exact_ratio else "partial"
                email = generate_training_email(args.category, match_type)
                if email:
                    emails.append(email)
            
            print(f"\nGenerated {len(emails)} emails for category: {args.category}")
            for email in emails:
                print(f"\n--- {email['match_type'].upper()} MATCH ---")
                print(f"Subject: {email['subject']}")
                print(f"Body: {email['body'][:200]}...")
                
                if args.test_api:
                    result = test_classification_api(email)
                    if result:
                        status = "✓ CORRECT" if result["correct"] else "✗ INCORRECT"
                        print(f"Predicted: {result['predicted']} (confidence: {result['confidence']:.2f}) {status}")
        else:
            print(f"Category '{args.category}' not found. Available categories:")
            for cat in TRAINING_TEMPLATES.keys():
                print(f"  - {cat}")
    else:
        # Generate full dataset
        dataset = generate_training_dataset(args.count, args.exact_ratio)
        
        print(f"Generated {len(dataset)} training emails across {len(TRAINING_TEMPLATES)} categories")
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(dataset, f, indent=2)
            print(f"Dataset saved to {args.output}")
        
        if args.test_api:
            print("\nTesting against API...")
            correct = 0
            total = 0
            
            for email in dataset[:20]:  # Test first 20 emails
                result = test_classification_api(email)
                if result:
                    total += 1
                    if result["correct"]:
                        correct += 1
                    
                    status = "✓" if result["correct"] else "✗"
                    print(f"{status} {email['category']} -> {result['predicted']} ({result['confidence']:.2f})")
            
            if total > 0:
                accuracy = correct / total * 100
                print(f"\nAccuracy: {accuracy:.1f}% ({correct}/{total})")

if __name__ == "__main__":
    main()