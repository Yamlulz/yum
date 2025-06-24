# Email Categorizer - Simple Setup Guide

## What This Does
This system reads your emails and automatically sorts them into business categories like "Complaint", "Sales Opportunity", "Urgent Action Needed", etc. It's like having a smart assistant that never gets tired of organizing your inbox.

## Why Use This?
- **Save Time**: No more manually sorting through hundreds of emails
- **Catch Important Stuff**: Never miss urgent complaints or sales opportunities
- **Stay Private**: Everything runs on your computer - no data sent to external companies
- **Get Smarter**: The system learns from your feedback and gets better over time

## What You Need
- A computer (Windows, Mac, or Linux)
- Internet connection (only for initial setup)
- About 30 minutes for setup

---

## Step 1: Get the Basic Stuff Ready

### Install Python (if you don't have it)
Python is like the engine that runs our email sorter.

**Windows:**
1. Go to python.org
2. Download Python (get the latest version)
3. Run the installer
4. ✅ Check "Add Python to PATH" during installation

**Mac:**
1. Open Terminal (search for "Terminal" in Spotlight)
2. Type: `brew install python` (if you have Homebrew)
3. Or download from python.org like Windows

**Check if Python is working:**
Open your command prompt/terminal and type:
```
python --version
```
You should see something like "Python 3.11.0"

### Install Required Libraries
These are like add-ons that help Python do specific tasks.

In your command prompt/terminal, type:
```
pip install flask requests
```

---

## Step 2: Set Up the Smart Brain (AI)

The "brain" of our system is called an LLM (Large Language Model). Think of it as a very smart robot that reads emails and understands what they're about.

### Option A: Automatic Setup (Recommended)
We made this super easy for you:

```bash
./setup_local_llm.sh
```

This script will:
- Download and install the AI brain (called "Ollama")
- Get a smart but lightweight model (about 2GB download)
- Test everything to make sure it works

### Option B: Manual Setup (if automatic doesn't work)

1. **Install Ollama** (the AI software):
   - Go to ollama.ai
   - Download for your operating system
   - Install it like any other program

2. **Start Ollama**:
   ```bash
   ollama serve
   ```

3. **Download the AI model**:
   ```bash
   ollama pull llama3.2:3b
   ```

### What's Happening Here?
- **Ollama**: Software that runs AI models on your computer
- **llama3.2:3b**: A smart AI model that's small enough to run quickly
- **Local**: Everything stays on your computer - no internet needed after setup

---

## Step 3: Start the Email Sorter

Now we'll start the actual email categorization service.

### Start the Main Program
In your terminal/command prompt, navigate to the email categorizer folder and type:
```bash
python backend/app.py
```

You should see something like:
```
* Running on http://127.0.0.1:5000
```

**What this means:** Your email sorter is now running and waiting for emails to categorize.

**Keep this window open** - this is your email sorter running in the background.

---

## Step 4: Test It Out

Let's make sure everything works before you start using it with real emails.

### Quick Test
Open a new terminal/command prompt window (keep the first one running) and type:
```bash
python demo_workflow.py
```

This will:
- Check if everything is working
- Generate some fake business emails
- Show you how the categorization works
- Give you accuracy scores

### What You'll See
The demo will show emails being sorted into categories like:
- ✅ "Complaint - Product/Service" (confidence: 85%)
- ✅ "Sales Opportunity - New Business" (confidence: 92%)
- ❌ "Action Required - Urgent Response" (confidence: 45%) - needs improvement

### Interactive Test
Want to try your own emails? Type:
```bash
python ui/cli_test.py
```

This lets you:
- Type in email subjects and content
- See how they get categorized
- Give feedback if the category is wrong

---

## Step 5: Understanding the Categories

Our system sorts emails into business-focused categories:

### 🚨 **Critical Issues** (Handle First!)
- **Complaints**: Unhappy customers, broken products, billing problems
- **Legal Problems**: Lawsuits, contract disputes, compliance issues
- **Crisis**: Security breaches, system outages, data problems
- **Reputation Risk**: Media inquiries, bad reviews going viral

### 💰 **Business Opportunities** (Don't Miss These!)
- **Sales**: New customers, upgrade requests, partnership offers
- **Good News**: Success stories, awards, happy customers
- **Renewals**: Contracts expiring, subscription opportunities

### ⚡ **Action Needed** (Someone Needs to Do Something!)
- **Urgent Response**: Emergencies, time-sensitive requests
- **Follow-up**: Waiting for updates, need to check progress
- **Executive Attention**: VIP customers, board-level decisions

### 🔧 **Day-to-Day Business**
- **Technical Support**: Bug reports, feature requests, help needed
- **Financial**: Invoice problems, payment issues, budget approvals
- **HR**: Employee issues, hiring, policy questions

---

## Step 6: Making It Better

The system gets smarter when you help it learn.

### Give Feedback
When the system gets something wrong:

1. Use the interactive test: `python ui/cli_test.py`
2. Enter the email details
3. See what category it picks
4. If it's wrong, tell it the right category
5. The system remembers and gets better

### Generate Training Data
Want to train it on specific types of emails? 

```bash
python generate_training_emails.py --category "Complaint - Product/Service" --count 10
```

This creates 10 realistic complaint emails to help the system learn.

---

## Step 7: Daily Usage

### Starting Your Day
1. Open terminal/command prompt
2. Start the AI brain: `ollama serve` (if not already running)
3. Start the email sorter: `python backend/app.py`
4. Your system is ready!

### Categorizing Emails
The system provides a web service that other programs can use. Soon, we'll have an Outlook add-in that automatically categorizes your emails as they arrive.

For now, you can:
- Test emails using the CLI tool
- Send emails to the API programmatically
- Use the demo to see how it works

### Stopping the System
- Press `Ctrl+C` in the terminal windows to stop
- Or just close the terminal windows

---

## Troubleshooting

### "Connection Refused" Error
**Problem:** The email sorter isn't running
**Solution:** Make sure you started it with `python backend/app.py`

### "Ollama Not Found" Error
**Problem:** The AI brain isn't installed or running
**Solution:** 
1. Install Ollama from ollama.ai
2. Start it with `ollama serve`
3. Download the model with `ollama pull llama3.2:3b`

### Slow Classifications
**Problem:** The AI is thinking hard
**Solution:** This is normal for the first few classifications. It gets faster.

### Wrong Categories
**Problem:** The system is learning
**Solution:** Give it feedback using the CLI tool. It will improve over time.

---

## What's Next?

### Outlook Integration (Coming Soon)
We're building an Outlook add-in that will:
- Automatically categorize emails as they arrive
- Add colored labels to your inbox
- Create smart folders for different categories
- Send alerts for urgent items

### Advanced Features
- Custom categories for your business
- Confidence thresholds (only show high-confidence classifications)
- Reporting and analytics
- Integration with other email systems

---

## Getting Help

### Check System Status
```bash
# Is the email sorter running?
curl http://127.0.0.1:5000/categories

# Is the AI brain running?
curl http://localhost:11434/api/tags
```

### Common Commands
```bash
# Start everything
ollama serve &
python backend/app.py

# Test the system
python demo_workflow.py

# Interactive testing
python ui/cli_test.py

# Generate training emails
python generate_training_emails.py --count 5 --test-api
```

### Files You Care About
- `backend/app.py` - The main email sorter program
- `backend/data/categories.json` - List of email categories
- `backend/data/feedback.json` - Your feedback to improve the system
- `README.md` - Technical documentation

---

## Summary

1. **Install Python and libraries** (one-time setup)
2. **Run the setup script** to get the AI brain (`./setup_local_llm.sh`)
3. **Start the email sorter** (`python backend/app.py`)
4. **Test it out** (`python demo_workflow.py`)
5. **Give feedback** to make it smarter
6. **Use it daily** to organize your emails

The system runs entirely on your computer, keeps your emails private, and gets better the more you use it. Think of it as training your own personal email assistant!