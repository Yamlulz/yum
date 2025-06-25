# YUM Email Categorizer - Local AI-Powered Business Email Classification

A privacy-focused email categorization system that uses local LLMs to intelligently classify business emails into actionable categories. Designed for integration with Outlook and other email systems.

## Business-Focused Email Categories

The system includes comprehensive business-focused categories designed to identify:

### Critical Business Issues
- **Complaints** (Product/Service, Billing/Payment, Staff/Customer Service)
- **Legal Escalation** (Contract Disputes, Compliance Issues, Litigation Threats)
- **Crisis Management** (Security Incidents, System Outages, Data Breaches)
- **Reputational Risk** (Media Inquiries, Social Media Issues, Public Complaints)

### Business Opportunities
- **Sales Opportunities** (New Business, Upsell/Cross-sell, Partnerships)
- **Good News** (Customer Success, Awards/Recognition, Positive Feedback)
- **Customer Retention** (Churn Risk, Renewal Opportunities)

### Action-Oriented Categories
- **Action Required** (Urgent Response, Follow-up Needed, Documentation)
- **Executive Attention** (VIP Customers, Strategic Decisions, Board Matters)
- **Financial** (Invoice Disputes, Payment Overdue, Budget Approval)
- **Technical Support** (Bug Reports, Feature Requests, Integration Issues)
- **HR** (Employee Issues, Recruitment, Policy Violations)
- **Regulatory** (Audit Requests, Compliance Reporting, License/Permit)
- **Vendor Management** (Contract Renewal, Performance Issues, New Suppliers)

## Setup and Installation

### 1. Install Local LLM (Recommended)
For accurate business email classification, set up a local LLM:
```bash
./setup_local_llm.sh
```
This installs Ollama and downloads a lightweight model (llama3.2:3b) for classification.

### 2. Install Python Dependencies
```bash
pip install flask requests
```

## Usage

### Starting the System
1. **Start Local LLM** (if using):
```bash
ollama serve
```

2. **Start the Flask Server**:
```bash
python backend/app.py
```
The server will run on `http://127.0.0.1:5000`

### Testing and Training

#### Interactive Testing
```bash
python ui/cli_test.py
```

#### Generate Training Data
Create realistic business emails for each category:
```bash
# Generate 5 emails per category (mix of exact and partial matches)
python generate_training_emails.py --count 5 --test-api

# Generate emails for specific category
python generate_training_emails.py --category "Complaint - Product/Service" --count 10

# Save training dataset to file
python generate_training_emails.py --count 10 --output training_data.json
```

#### Test LLM Classification
```bash
# Test if local LLM is working
python test_llm_classification.py

# Generate and test emails against API
python generate_training_emails.py --test-api --count 3
```

#### Legacy Email Generation (Simple)
```bash
# Generate 1 random email
./generate_email.sh

# Generate 5 realistic emails
./generate_realistic_emails.sh 5
```

### API Endpoints
- `POST /classify` - Classify an email using LLM (requires `subject` and `body`)
- `POST /feedback` - Submit feedback for model improvement (requires `email` and `correct_category`)
- `GET /categories` - Get all available business categories
- `POST /category` - Add a new category (requires `name`)

## Architecture

### LLM-Based Classification
The system uses a local LLM (Ollama with llama3.2:3b) for intelligent email classification:
- **Primary**: Local LLM with business-focused prompts
- **Fallback**: Keyword-based classification if LLM unavailable
- **Privacy**: All processing happens locally, no external API calls

### Training Data Generation
The `generate_training_emails.py` script creates realistic business emails with:
- **Exact Matches**: Clear, unambiguous examples for each category
- **Partial Matches**: Subtle or mixed signals to test classification boundaries
- **Variations**: Random additions (urgency prefixes, company names, reference numbers)

### Feedback Loop
User feedback is collected and stored (with email content hashed for privacy) to:
- Improve classification accuracy
- Identify misclassified emails
- Train future model iterations

## Files Structure

```
yum/
├── backend/
│   ├── app.py                 # Flask API server
│   ├── categoriser.py         # LLM-based classification logic
│   └── data/
│       ├── categories.json    # Business category definitions
│       └── feedback.json      # User feedback (hashed)
├── ui/
│   └── cli_test.py           # Interactive testing interface
├── generate_training_emails.py # Advanced training data generator
├── setup_local_llm.sh        # LLM installation script
├── test_llm_classification.py # LLM testing script (created by setup)
├── generate_email.sh         # Simple email generator
└── generate_realistic_emails.sh # Realistic email generator
```

## Privacy and Security

- **Local Processing**: All email classification happens locally
- **No External APIs**: No data sent to external services
- **Content Hashing**: Email content is hashed before storage
- **Secure Feedback**: User corrections stored without raw email data

## Troubleshooting

### LLM Issues
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
ollama serve

# List installed models
ollama list
```

### API Issues
```bash
# Test API directly
curl -X POST http://127.0.0.1:5000/classify \
  -H "Content-Type: application/json" \
  -d '{"subject":"Test","body":"This is a test email"}'
```

## Changes Made

*   Replaced simple categories with comprehensive business-focused categories
*   Implemented LLM-based classification using local Ollama
*   Created advanced training data generator with realistic business emails
*   Added fallback classification for when LLM is unavailable
*   Enhanced privacy with email content hashing
*   Added comprehensive setup and testing scripts
*   Improved error handling and logging throughout the system