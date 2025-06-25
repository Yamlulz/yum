# Automated Training System Guide

This guide explains how to use the new automated training system that uses API calls to generate emails, classify them, and apply feedback to train the email categorization model.

## Overview

The automated training system performs a complete training workflow using 3 API calls:

1. **📧 Generate Emails** - Uses external LLM API to create realistic training emails
2. **🎯 Classify Emails** - Uses the current model to classify each generated email  
3. **📚 Apply Feedback** - Saves feedback for incorrect classifications to improve the model

## Quick Start

### 1. Setup
```bash
# Ensure backend is running
python backend/app.py

# Set your OpenAI API key
export OPENAI_API_KEY='your-api-key-here'
```

### 2. Run Demo
```bash
# Interactive demo showing the training workflow
python demo_automated_training.py
```

### 3. Run Automated Training
```bash
# Single training cycle with 10 emails
python automated_training_system.py --single-cycle --emails-per-cycle 10

# Continuous training with 5 cycles
python automated_training_system.py --cycles 5 --emails-per-cycle 8
```

## API Workflow Details

### API Call 1: Generate Training Emails
```bash
POST /generate-emails
{
  "count": 10
}
```

**Response:**
- `emails`: Array of generated emails without category labels
- `answer_key`: Array with correct categories for validation
- `categories`: Available categories for classification

### API Call 2: Classify Emails
```bash
POST /classify
{
  "subject": "Email subject",
  "body": "Email body content"
}
```

**Response:**
- `category`: Predicted category
- `confidence`: Classification confidence score

### API Call 3: Apply Feedback
```bash
POST /feedback
{
  "email": {"subject": "...", "body": "..."},
  "correct_category": "Correct Category Name"
}
```

**Response:**
- `status`: Success/failure status

## Training System Features

### 🔄 Single Training Cycle
Runs one complete training cycle:
```bash
python automated_training_system.py --single-cycle --emails-per-cycle 15
```

**Process:**
1. Generates specified number of emails
2. Classifies each email using current model
3. Applies feedback for incorrect classifications
4. Reports accuracy and training metrics

### 🔁 Continuous Training
Runs multiple training cycles with delays:
```bash
python automated_training_system.py --cycles 10 --emails-per-cycle 5 --delay 60
```

**Process:**
1. Runs specified number of cycles
2. Waits between cycles for model adaptation
3. Tracks accuracy improvement over time
4. Provides comprehensive training statistics

### 📊 Training Statistics
The system tracks:
- Total emails generated and processed
- Classification accuracy over time
- Feedback corrections applied
- Training session duration and performance

## Command Line Options

### Basic Options
```bash
--backend-url URL          # Backend server URL (default: http://localhost:5000)
--cycles N                 # Number of training cycles (default: 3)
--emails-per-cycle N       # Emails per cycle (default: 10)
--delay N                  # Seconds between cycles (default: 30)
```

### Training Modes
```bash
--single-cycle             # Run only one training cycle
--save-stats FILE          # Save training statistics to file
```

## Usage Examples

### Example 1: Quick Training Session
```bash
# Run 3 cycles with 5 emails each, 15 second delays
python automated_training_system.py --cycles 3 --emails-per-cycle 5 --delay 15
```

### Example 2: Intensive Training
```bash
# Single cycle with many emails for intensive feedback
python automated_training_system.py --single-cycle --emails-per-cycle 25
```

### Example 3: Long-term Training
```bash
# Extended training with statistics saving
python automated_training_system.py --cycles 20 --emails-per-cycle 8 --delay 120 --save-stats long_training.json
```

## Demo Options

The demo script provides interactive examples:

```bash
python demo_automated_training.py
```

**Demo Options:**
1. **Single Training Cycle** - Shows one complete cycle with 5 emails
2. **Continuous Training** - Shows 3 cycles with progress tracking
3. **API Workflow Breakdown** - Shows individual API calls step-by-step
4. **Run All Demos** - Comprehensive demonstration

## Training Results

### Accuracy Tracking
The system tracks accuracy improvements:
```
📊 CONTINUOUS TRAINING RESULTS:
✅ Successful cycles: 5/5
📧 Total emails: 50
🎯 Total classifications: 50
📚 Total feedback applied: 12
📊 Average accuracy: 76.2%
📈 Accuracy trend: 68.0% → 84.0%
```

### Session Statistics
Each training session records:
- Timestamp and duration
- Email count and classification count
- Accuracy achieved
- Feedback corrections applied

## Troubleshooting

### Backend Connection Issues
```bash
# Check if backend is running
curl http://localhost:5000/categories

# Start backend if needed
python backend/app.py
```

### API Key Issues
```bash
# Check if API key is set
echo $OPENAI_API_KEY

# Set API key
export OPENAI_API_KEY='your-key-here'
```

### Email Generation Failures
- Ensure internet connectivity
- Verify API key has sufficient credits
- Check API rate limits

### Classification Failures
- Ensure local LLM (Ollama) is running if using local classification
- Check backend logs for detailed error messages

## Advanced Usage

### Custom Training Parameters
You can modify the training system for specific needs:

```python
from automated_training_system import AutomatedTrainingSystem

trainer = AutomatedTrainingSystem("http://localhost:5000")

# Custom training cycle
result = trainer.run_training_cycle(email_count=20)

# Custom continuous training
results = trainer.run_continuous_training(
    cycles=10,
    emails_per_cycle=15,
    delay_between_cycles=45
)
```

### Batch Feedback Processing
For efficient training, use the batch feedback endpoint:

```bash
POST /batch-feedback
{
  "feedback_items": [
    {
      "email": {"subject": "...", "body": "..."},
      "correct_category": "Category Name"
    }
  ]
}
```

## Integration with Existing Workflow

The automated training system integrates with:

1. **Manual Training Tool** - `email_training_tool.py`
2. **Template-based Generator** - `generate_training_emails.py`
3. **Classification API** - `/classify` endpoint
4. **Feedback System** - `/feedback` endpoint

## Performance Considerations

### API Rate Limits
- OpenAI API has rate limits - adjust delays accordingly
- Monitor API usage and costs
- Consider using GPT-3.5-turbo for cost efficiency

### Training Frequency
- Run training cycles regularly but not excessively
- Allow time between cycles for model adaptation
- Monitor accuracy trends to optimize frequency

### Resource Usage
- Each email generation uses API tokens
- Classification uses local compute resources
- Feedback storage grows over time

## Best Practices

1. **Start Small** - Begin with 5-10 emails per cycle
2. **Monitor Progress** - Track accuracy improvements
3. **Regular Training** - Run cycles consistently
4. **Save Statistics** - Keep records of training sessions
5. **Balance Load** - Don't overwhelm the API or local resources

---

## Quick Reference

```bash
# Demo the system
python demo_automated_training.py

# Single training cycle
python automated_training_system.py --single-cycle --emails-per-cycle 10

# Continuous training
python automated_training_system.py --cycles 5 --emails-per-cycle 8 --delay 30

# Save training stats
python automated_training_system.py --cycles 3 --save-stats training_results.json
```

Happy training! 🚀