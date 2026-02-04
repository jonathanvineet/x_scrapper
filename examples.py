#!/usr/bin/env python3
"""
Example: How to use the generic scraper for different topics
Run any of these examples!
"""

# ============================================================================
# EXAMPLE 1: Sports & Entertainment
# ============================================================================
print("""
EXAMPLE 1: Sports Tweets
python generic_scraper.py -a "NBA,ESPN,NFL" -m 10 -d sports.db
""")

# ============================================================================
# EXAMPLE 2: Technology News
# ============================================================================
print("""
EXAMPLE 2: Tech Company Accounts
python generic_scraper.py -a "Apple,Google,Microsoft" -m 15 -d tech.db
""")

# ============================================================================
# EXAMPLE 3: News & Media
# ============================================================================
print("""
EXAMPLE 3: News Organizations
python generic_scraper.py -a "CNN,BBCWorld,Reuters,AP" -m 20 -d news.db
""")

# ============================================================================
# EXAMPLE 4: Business & Finance
# ============================================================================
print("""
EXAMPLE 4: Business Accounts
python generic_scraper.py -a "business,Forbes,WSJ,Bloomberg" -m 15 -d business.db
""")

# ============================================================================
# EXAMPLE 5: Science & Space
# ============================================================================
print("""
EXAMPLE 5: Science Accounts
python generic_scraper.py -a "NASA,SpaceX,NatGeo,CERN" -m 10 -d science.db
""")

# ============================================================================
# EXAMPLE 6: With Keyword Filtering
# ============================================================================
print("""
EXAMPLE 6: Filter Account Tweets by Keywords
python generic_scraper.py -a "NBA,ESPN" -k "playoffs,championship" -m 15
""")

# ============================================================================
# EXAMPLE 7: Using Config File
# ============================================================================
print("""
EXAMPLE 7: Use Configuration File
Create my_search.json:
{
  "accounts": ["account1", "account2"],
  "keywords": ["keyword1", "keyword2"],
  "max_tweets": 20,
  "database": "my_results.db"
}

Then run:
python generic_scraper.py -c my_search.json
""")

# ============================================================================
# EXAMPLE 8: Interactive Mode
# ============================================================================
print("""
EXAMPLE 8: Interactive Mode (Easiest!)
python generic_scraper.py

Then just answer the prompts:
- Enter keywords (or skip)
- Enter accounts (or skip)  
- Set max tweets
- Set database name
""")

# ============================================================================
# EXAMPLE 9: Silent Mode (No Display)
# ============================================================================
print("""
EXAMPLE 9: Scrape Silently (Large Datasets)
python generic_scraper.py -a "account1,account2,account3" -m 50 --no-display
""")

# ============================================================================
# EXAMPLE 10: Multiple Sequential Scrapes
# ============================================================================
print("""
EXAMPLE 10: Run Multiple Scrapes
python generic_scraper.py -a "NBA,NFL" -d sports.db
python generic_scraper.py -a "CNN,BBC" -d news.db
python generic_scraper.py -a "NASA,SpaceX" -d space.db
""")

print("""
============================================================================
✨ THE SCRAPER IS 100% GENERIC!

You can scrape:
- ANY keywords
- ANY accounts
- ANY topics
- ANY combination

Just replace the examples above with YOUR interests!
============================================================================
""")

# ============================================================================
# Quick Test Function
# ============================================================================
def quick_test():
    """Run a quick test to verify the scraper works"""
    import subprocess
    
    print("\n🧪 Quick Test: Scraping 3 tweets from ESPN")
    print("Command: python generic_scraper.py -a 'ESPN' -m 3 -d test.db\n")
    
    choice = input("Run this test? (y/n): ").strip().lower()
    if choice == 'y':
        subprocess.run([
            'python', 'generic_scraper.py',
            '-a', 'ESPN',
            '-m', '3',
            '-d', 'test.db'
        ])
        print("\n✅ Test complete! Check test.db")
    else:
        print("Test skipped")

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("📖 GENERIC SCRAPER - EXAMPLES")
    print("=" * 70)
    
    quick_test()
