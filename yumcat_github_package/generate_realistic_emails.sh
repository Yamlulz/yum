#!/bin/bash

# Arrays of realistic email components
subjects=(
    "Urgent: System maintenance required"
    "Meeting request for next week"
    "Invoice #12345 - Payment due"
    "Customer complaint about product quality"
    "Sales opportunity - New client inquiry"
    "Technical support request"
    "Project update and next steps"
    "Password reset request"
    "Order confirmation #67890"
    "Feedback on recent service"
)

bodies=(
    "Dear team, we need to schedule urgent maintenance for our servers this weekend. Please confirm your availability."
    "Hi, I would like to schedule a meeting to discuss the upcoming project milestones. Are you available next Tuesday?"
    "This is a reminder that invoice #12345 for $2,500 is due within 5 days. Please process payment at your earliest convenience."
    "I am writing to express my dissatisfaction with the product I received. The quality does not meet expectations."
    "We have a potential new client interested in our services. They are looking for a comprehensive solution for their business needs."
    "I am experiencing technical difficulties with the software. The application crashes when I try to export data."
    "Here is the latest update on our project progress. We have completed phase 1 and are moving to phase 2 next week."
    "I forgot my password and need to reset it. Please send me instructions on how to regain access to my account."
    "Thank you for your order. Your items will be shipped within 2-3 business days to the address provided."
    "We would appreciate your feedback on the service you received. Your input helps us improve our offerings."
)

# Number of emails to generate (default: 5)
count=${1:-5}

echo "Generating $count realistic emails..."
echo "=================================="

for i in $(seq 1 $count); do
    # Select random subject and body
    subject_index=$((RANDOM % ${#subjects[@]}))
    body_index=$((RANDOM % ${#bodies[@]}))
    
    subject="${subjects[$subject_index]}"
    body="${bodies[$body_index]}"
    
    # Format the data as JSON
    data=$(cat <<EOF
{
  "subject": "$subject",
  "body": "$body"
}
EOF
)
    
    echo "Email #$i:"
    echo "Subject: $subject"
    echo "Body: $body"
    
    # Send the data to the API
    response=$(curl -s -X POST -H "Content-Type: application/json" -d "$data" http://127.0.0.1:5000/classify 2>/dev/null)
    
    if [ $? -eq 0 ] && [ -n "$response" ]; then
        # Parse the response
        category=$(echo "$response" | jq -r .category 2>/dev/null)
        confidence=$(echo "$response" | jq -r .confidence 2>/dev/null)
        
        echo "Category: $category"
        echo "Confidence: $confidence"
    else
        echo "Error: Could not connect to API or invalid response"
    fi
    
    echo "--------------------------------"
done

echo "Done generating $count emails!"