#!/usr/bin/env python3
"""
Quick demo script showing the generic scraper's versatility
"""

import subprocess
import sys

demos = [
    {
        'name': 'Sports',
        'cmd': ['python', 'generic_scraper.py', '-k', 'NBA,football', '-m', '5', '-d', 'demo_sports.db', '--no-display'],
        'desc': 'Scraping sports tweets about NBA and football'
    },
    {
        'name': 'Technology',
        'cmd': ['python', 'generic_scraper.py', '-k', 'iPhone,Android', '-m', '5', '-d', 'demo_tech.db', '--no-display'],
        'desc': 'Scraping tech tweets about smartphones'
    },
    {
        'name': 'Entertainment',
        'cmd': ['python', 'generic_scraper.py', '-k', 'Marvel,Netflix', '-m', '5', '-d', 'demo_entertainment.db', '--no-display'],
        'desc': 'Scraping entertainment tweets'
    },
    {
        'name': 'Business',
        'cmd': ['python', 'generic_scraper.py', '-a', 'business,Forbes', '-m', '5', '-d', 'demo_business.db', '--no-display'],
        'desc': 'Scraping business accounts'
    }
]

print("\n" + "=" * 70)
print("🎯 GENERIC SCRAPER DEMO - Works for ANY Topic!")
print("=" * 70)

for i, demo in enumerate(demos, 1):
    print(f"\n{i}. {demo['name']}: {demo['desc']}")
    print(f"   Command: {' '.join(demo['cmd'])}")
    
    choice = input(f"   Run this demo? (y/n): ").strip().lower()
    if choice == 'y':
        print(f"   Running...")
        try:
            result = subprocess.run(demo['cmd'], capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                print(f"   ✅ Success! Check {demo['cmd'][-3]}")
            else:
                print(f"   ⚠️  Check output: {result.stderr[:100]}")
        except subprocess.TimeoutExpired:
            print(f"   ⏱️  Timeout - this may take longer")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    else:
        print(f"   ⏭️  Skipped")

print("\n" + "=" * 70)
print("✅ Demo complete!")
print("=" * 70)
print("\nYou can search for ANYTHING:")
print("  • Politics: python generic_scraper.py -k 'election,congress'")
print("  • Health: python generic_scraper.py -k 'fitness,nutrition'")
print("  • Travel: python generic_scraper.py -k 'vacation,tourism'")
print("  • Fashion: python generic_scraper.py -k 'fashion,style'")
print("  • Gaming: python generic_scraper.py -k 'gaming,esports'")
print("  • ... literally ANYTHING!")
print("=" * 70 + "\n")
