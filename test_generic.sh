#!/bin/bash
# Quick test examples for the generic scraper

echo "========================================"
echo "🧪 TESTING GENERIC SCRAPER"
echo "========================================"

# Example 1: Politics
echo -e "\n1️⃣ Testing: Politics"
python generic_scraper.py -k "election,congress,senate" -m 5 -d test_politics.db --no-display

# Example 2: Technology  
echo -e "\n2️⃣ Testing: Technology"
python generic_scraper.py -k "iPhone,Android,Samsung" -m 5 -d test_tech.db --no-display

# Example 3: Sports
echo -e "\n3️⃣ Testing: Sports"
python generic_scraper.py -k "NBA,football,playoffs" -m 5 -d test_sports.db --no-display

# Example 4: Entertainment
echo -e "\n4️⃣ Testing: Entertainment"
python generic_scraper.py -k "movies,Netflix,streaming" -m 5 -d test_entertainment.db --no-display

# Example 5: Business
echo -e "\n5️⃣ Testing: Business"
python generic_scraper.py -k "stocks,market,economy" -m 5 -d test_business.db --no-display

echo -e "\n========================================"
echo "✅ All tests complete! Check the test_*.db files"
echo "========================================"
