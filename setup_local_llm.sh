#!/bin/bash

# Setup script for local LLM with Ollama
# This script installs Ollama and downloads a lightweight model for email classification

set -e

echo "🤖 Setting up Local LLM for Email Categorization"
echo "================================================"

# Check if Ollama is already installed
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is already installed"
else
    echo "📦 Installing Ollama..."
    
    # Install Ollama based on OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -fsSL https://ollama.ai/install.sh | sh
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Please install Ollama manually from https://ollama.ai/download"
        echo "Or use: brew install ollama"
        exit 1
    else
        echo "❌ Unsupported OS. Please install Ollama manually from https://ollama.ai"
        exit 1
    fi
fi

# Start Ollama service
echo "🚀 Starting Ollama service..."
ollama serve &
OLLAMA_PID=$!

# Wait for service to start
echo "⏳ Waiting for Ollama to start..."
sleep 5

# Function to check if Ollama is running
check_ollama() {
    curl -s http://localhost:11434/api/tags > /dev/null 2>&1
}

# Wait for Ollama to be ready
for i in {1..30}; do
    if check_ollama; then
        echo "✅ Ollama is running"
        break
    fi
    echo "⏳ Waiting for Ollama to be ready... ($i/30)"
    sleep 2
done

if ! check_ollama; then
    echo "❌ Failed to start Ollama service"
    exit 1
fi

# Download lightweight model for email classification
echo "📥 Downloading lightweight model (llama3.2:3b)..."
echo "This may take a few minutes depending on your internet connection..."

ollama pull llama3.2:3b

if [ $? -eq 0 ]; then
    echo "✅ Model downloaded successfully"
else
    echo "❌ Failed to download model"
    exit 1
fi

# Test the model with a sample classification
echo "🧪 Testing model with sample email classification..."

cat > test_prompt.txt << 'EOF'
You are an expert email classifier for business communications. 

Analyze this email and classify it into ONE of the following categories:

- Complaint - Product/Service
- Sales Opportunity - New Business
- Action Required - Urgent Response
- General Inquiry

Email Subject: Product not working properly
Email Body: Hi, I bought your product last week but it's not functioning as expected. Can you help?

Instructions:
1. Choose the MOST APPROPRIATE category from the list above
2. Respond with ONLY the category name, exactly as listed above

Category:
EOF

# Test the model
TEST_RESULT=$(ollama run llama3.2:3b < test_prompt.txt)
echo "🔍 Test classification result: $TEST_RESULT"

# Clean up test file
rm test_prompt.txt

# Create a simple test script
cat > test_llm_classification.py << 'EOF'
#!/usr/bin/env python3
import requests
import json

def test_ollama_classification():
    """Test Ollama classification with a sample email"""
    
    prompt = """You are an expert email classifier for business communications. 

Analyze this email and classify it into ONE of the following categories:

- Complaint - Product/Service
- Sales Opportunity - New Business
- Action Required - Urgent Response
- General Inquiry

Email Subject: Urgent: System Down
Email Body: Our production system is completely down and we need immediate assistance. This is affecting all our customers.

Instructions:
1. Choose the MOST APPROPRIATE category from the list above
2. Respond with ONLY the category name, exactly as listed above

Category:"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.2:3b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "max_tokens": 50
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            classification = result.get("response", "").strip()
            print(f"✅ LLM Classification: {classification}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing LLM Classification...")
    success = test_ollama_classification()
    if success:
        print("✅ Local LLM is working correctly!")
    else:
        print("❌ Local LLM test failed")
EOF

chmod +x test_llm_classification.py

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "✅ Ollama installed and running"
echo "✅ llama3.2:3b model downloaded"
echo "✅ Test script created: test_llm_classification.py"
echo ""
echo "📋 Next Steps:"
echo "1. Test the LLM: python3 test_llm_classification.py"
echo "2. Start your Flask server: python3 backend/app.py"
echo "3. Generate training emails: python3 generate_training_emails.py --test-api"
echo ""
echo "💡 Tips:"
echo "- Ollama runs on http://localhost:11434"
echo "- The model uses minimal resources (3B parameters)"
echo "- You can stop Ollama with: pkill ollama"
echo "- To restart Ollama: ollama serve"
echo ""
echo "🔧 Troubleshooting:"
echo "- If classification fails, check if Ollama is running: curl http://localhost:11434/api/tags"
echo "- View Ollama logs: journalctl -u ollama -f (on systemd systems)"
echo "- List installed models: ollama list"

# Keep Ollama running in background
echo "🔄 Ollama is running in background (PID: $OLLAMA_PID)"
echo "To stop: kill $OLLAMA_PID"