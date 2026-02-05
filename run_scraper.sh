#!/bin/bash

# Navigate to scraper directory
cd "$(dirname "$0")"

# Log file
LOG_FILE="scraper.log"

# Run the scraper
echo "========================================" >> "$LOG_FILE"
echo "Scraper started at $(date)" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"

python3 scrape_crypto_fast.py >> "$LOG_FILE" 2>&1

if [ $? -eq 0 ]; then
    echo "Scraper completed successfully at $(date)" >> "$LOG_FILE"
else
    echo "Scraper failed at $(date)" >> "$LOG_FILE"
fi

echo "" >> "$LOG_FILE"
