#!/bin/bash

# Generate random email content
subject=$(head /dev/urandom | tr -dc A-Za-z0-9\  | head -c 20)
body=$(head /dev/urandom | tr -dc A-Za-z0-9\  | head -c 100)

# Format the data as JSON
data=$(cat <<EOF
{
  "subject": "$subject",
  "body": "$body"
}
EOF
)

# Send the data to the API
response=$(curl -X POST -H "Content-Type: application/json" -d "$data" http://127.0.0.1:5000/classify)

# Parse the response
category=$(echo "$response" | jq -r .category)
confidence=$(echo "$response" | jq -r .confidence)

# Print the results
echo "Subject: $subject"
echo "Body: $body"
echo "Category: $category"
echo "Confidence: $confidence"