#!/bin/bash -eu

# Example of execution: 
# bash infra/get_last_price.sh "https://www.google.com/finance/quote/EUR-USD"

# Check if URL is provided
if [ "$#" -ne 1 ] || [ -z "$1" ]; then
    echo "Usage: $0 URL"
    exit 1
fi

# Define the URL to which the GET request will be made
url=$1

# Make the GET request using curl
pageContent=$(curl -s "$url" || true)

# Uncomment the next line if you need to see the fetched page content
# echo "$pageContent"

# Extract the value of data-last-price using sed
price=$(echo "$pageContent" | sed -n 's/.*data-last-price="\([0-9.]*\)".*/\1/p')

# Debug output to help diagnose extraction issues
if [ -z "$price" ]; then
    echo "Debug: Page content may not contain data-last-price attribute."
    echo "Page content (truncated):"
    echo "$pageContent" | head -n 20
fi

# Check if the price was extracted
if [ -z "$price" ]; then
    echo "Could not extract the data-last-price value"
    exit 1
fi

# Print only the extracted price
echo "$price"



