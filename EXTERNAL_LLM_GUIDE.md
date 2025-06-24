# External LLM Email Generator Guide

This guide explains how to use the new external LLM functionality to generate realistic training emails for categorization practice.

## Quick Setup

1. **Install dependencies**:
   ```bash
   python setup_external_llm.py
   ```

2. **Set your OpenAI API key**:
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

3. **Start the backend**:
   ```bash
   python backend/app.py
   ```

4. **Generate and categorize emails**:
   ```bash
   python email_training_tool.py --count 10
   ```

## Features

### 🎯 Interactive Training
- Generate realistic emails using GPT models
- Practice categorizing emails with immediate feedback
- Get accuracy scores and performance analysis
- Learn from mistakes with correct answers

### 📧 Flexible Email Generation
- Specify exactly how many emails you want (1-50)
- Generate emails across all categories or specific ones
- Different difficulty levels (easy, medium, hard)
- More realistic and varied than template-based emails

### 🔧 API Integration
- REST API endpoints for email generation
- Easy integration with existing systems
- Validation endpoints for checking categorizations

## Usage Examples

### Basic Training Session
```bash
# Generate 15 emails for practice
python email_training_tool.py --count 15
```

### Generate Specific Category
```bash
# Generate 5 sales opportunity emails
python backend/email_generator.py --category "Sales Opportunity - New Business" --count 5
```

### Save Training Session
```bash
# Generate emails and save session
python email_training_tool.py --count 10 --save my_session.json

# Load saved session later
python email_training_tool.py --load my_session.json
```

### API Usage
```bash
# Generate emails via API
curl -X POST http://localhost:5000/generate-emails \
  -H "Content-Type: application/json" \
  -d '{"count": 5}'

# Validate categorizations
curl -X POST http://localhost:5000/validate-categorization \
  -H "Content-Type: application/json" \
  -d '{
    "categorizations": [{"id": 1, "category": "Sales Opportunity - New Business"}],
    "answer_key": [{"id": 1, "correct_category": "Sales Opportunity - New Business"}]
  }'
```

## Training Workflow

1. **Generate Emails**: Use the tool to create realistic business emails
2. **Categorize**: Read each email and assign it to a business category
3. **Get Feedback**: See which ones you got right/wrong
4. **Learn**: Review correct answers for missed categorizations
5. **Practice**: Repeat with different email sets to improve

## Categories Available

The system includes 45+ business-focused categories:

**Critical Issues:**
- Complaint - Product/Service
- Legal Escalation - Threat/Litigation
- Crisis Management - Security Incident
- Reputational Risk - Media Inquiry

**Business Opportunities:**
- Sales Opportunity - New Business
- Sales Opportunity - Upsell/Cross-sell
- Good News - Customer Success

**Action Required:**
- Action Required - Urgent Response
- Executive Attention - VIP Customer
- Financial - Payment Overdue
- Technical Support - Bug Report

And many more...

## Tips for Better Training

1. **Start Small**: Begin with 5-10 emails to get familiar
2. **Read Carefully**: Pay attention to tone, urgency, and business context
3. **Learn from Mistakes**: Review incorrect categorizations to understand patterns
4. **Practice Regularly**: Consistent practice improves categorization skills
5. **Try Different Difficulties**: Mix easy, medium, and hard emails

## Troubleshooting

### API Key Issues
```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Set API key (Unix/Linux/Mac)
export OPENAI_API_KEY='your-key-here'

# Set API key (Windows)
set OPENAI_API_KEY=your-key-here
```

### Backend Connection Issues
```bash
# Check if backend is running
curl http://localhost:5000/categories

# Start backend if not running
python backend/app.py
```

### Generation Failures
- Ensure you have internet connectivity
- Check API key is valid and has credits
- Try reducing the number of emails requested
- Check backend logs for detailed error messages

## Cost Considerations

- GPT-3.5-turbo: ~$0.001-0.002 per email generated
- GPT-4: ~$0.01-0.03 per email generated
- 10 emails typically costs less than $0.05 with GPT-3.5-turbo

## Advanced Usage

### Custom Configuration
Create `email_generator_config.json`:
```json
{
  "api_provider": "openai",
  "model": "gpt-3.5-turbo",
  "default_email_count": 10,
  "difficulty_distribution": {
    "easy": 0.3,
    "medium": 0.5,
    "hard": 0.2
  }
}
```

### Batch Processing
```python
from backend.email_generator import EmailGenerator

generator = EmailGenerator()
emails = generator.generate_emails_batch(count=50)
```

## Benefits Over Template-Based Generation

1. **More Realistic**: LLM-generated emails sound more natural
2. **Greater Variety**: Each email is unique, not based on templates
3. **Better Training**: More challenging and realistic scenarios
4. **Scalable**: Can generate unlimited variations
5. **Contextual**: Emails include realistic business details and scenarios

---

Happy training! 🚀