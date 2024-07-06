#!/bin/bash -eu

# Function to test the main script
test_get_last_price() {
    local url=$1
    local expected_pattern=$2

    # Run the main script with the provided URL
    result=$(./infra/get_last_price.sh "$url" 2>&1 || true)

    # Check if the result matches the expected pattern
    if [[ "$result" =~ $expected_pattern ]]; then
        echo "Test passed: $url"
    else
        echo "Test failed: $url"
        echo "Expected: $expected_pattern"
        echo "Got: $result"
    fi
}

# Test cases
test_get_last_price "" "Usage: ./infra/get_last_price.sh URL"
test_get_last_price "invalid-url" "Could not extract the data-last-price value"
test_get_last_price "https://www.google.com/finance/quote/EUR-USD" "^[0-9.]+$"
