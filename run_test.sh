#!/bin/bash

echo "🧪 Starting Unit Tests for All Microservices..."

# List of microservice folders
services=(
    "ocr-service"
    "drug-extractor-service"
    "medicine-detection-service"
    "drug-interaction-service"
    "gateway"
)

FAILED=()

for service in "${services[@]}"
do
    echo "🔍 Running tests for $service..."
    
    if [ -d "$service/tests" ]; then
        (cd $service && pytest tests/)
        if [ $? -ne 0 ]; then
            FAILED+=("$service")
        fi
    else
        echo "⚠️ No tests found for $service."
    fi
done

if [ ${#FAILED[@]} -ne 0 ]; then
    echo ""
    echo "❌ Tests failed in the following services:"
    for fail in "${FAILED[@]}"
    do
        echo "- $fail"
    done
    exit 1
else
    echo ""
    echo "✅ All tests passed successfully!"
    exit 0
fi

# Note: Make sure to give execute permission to this script before running it.
# chmod +x run_test.sh
# Usage: ./run_test.sh