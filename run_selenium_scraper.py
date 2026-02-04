#!/usr/bin/env python3
"""
Test Selenium setup and scrape recent crypto tweets
"""

import sys
import logging
from datetime import datetime, timedelta
from config import Config
from crypto_scraper_orchestrator import CryptoTwitterIntelligence

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    print("=" * 70)
    print("🚀 CRYPTO TWITTER SCRAPER - SELENIUM MODE")
    print("=" * 70)
    
    # Load config from environment
    config = {
        'use_api': Config.USE_API,
        'use_selenium': Config.USE_SELENIUM,
        'headless': Config.HEADLESS,
        'database_path': Config.DATABASE_PATH,
        'scraping_config': {
            'max_tweets_per_account': Config.MAX_TWEETS_PER_ACCOUNT,
            'scroll_pause_time': Config.SCROLL_PAUSE_TIME,
        }
    }
    
    print(f"\n📊 Configuration:")
    print(f"   • USE_API: {config['use_api']}")
    print(f"   • USE_SELENIUM: {config['use_selenium']}")
    print(f"   • HEADLESS: {config['headless']}")
    print(f"   • MAX_TWEETS: {config['scraping_config']['max_tweets_per_account']}")
    
    if not config['use_selenium']:
        print("\n❌ Selenium is disabled in .env file!")
        print("   Set USE_SELENIUM=true in .env")
        return
    
    print("\n🔧 Initializing scraper...")
    scraper = CryptoTwitterIntelligence(config)
    
    # Top crypto accounts to scrape
    accounts_to_scrape = [
        'VitalikButerin',
        'cz_binance', 
        'APompliano',
        'elonmusk',
        'Saylor',
        'aantonop',
        'balajis',
        'CathieDWood'
    ]
    
    print(f"\n📱 Scraping {len(accounts_to_scrape)} crypto influencer accounts...")
    print(f"   Looking for tweets from the last 2 days\n")
    
    total_tweets = 0
    two_days_ago = datetime.now() - timedelta(days=2)
    
    for i, username in enumerate(accounts_to_scrape, 1):
        print(f"\n[{i}/{len(accounts_to_scrape)}] 🔍 Scraping @{username}...")
        
        try:
            tweets = scraper.scrape_account(username, max_tweets=20)
            
            # Filter for tweets from last 2 days
            recent_tweets = [
                t for t in tweets 
                if isinstance(t.timestamp, datetime) and t.timestamp >= two_days_ago
            ]
            
            if recent_tweets:
                print(f"   ✅ Found {len(recent_tweets)} recent tweets")
                
                # Show top 3 tweets
                for j, tweet in enumerate(recent_tweets[:3], 1):
                    print(f"\n   Tweet {j}:")
                    print(f"   📅 {tweet.timestamp.strftime('%Y-%m-%d %H:%M')}")
                    print(f"   💬 {tweet.text[:150]}{'...' if len(tweet.text) > 150 else ''}")
                    print(f"   ❤️  {tweet.likes} | 🔄 {tweet.retweets} | 😊 {tweet.sentiment_label}")
                
                total_tweets += len(recent_tweets)
            else:
                print(f"   ⚠️  No recent tweets found (might need more scrolling)")
                
        except Exception as e:
            print(f"   ❌ Error: {str(e)[:100]}")
            continue
    
    print("\n" + "=" * 70)
    print(f"✅ SCRAPING COMPLETE!")
    print(f"   • Total recent tweets collected: {total_tweets}")
    print(f"   • Database: {config['database_path']}")
    print("=" * 70)
    
    # Show analytics
    if total_tweets > 0:
        print("\n📊 Generating analytics...")
        try:
            analytics = scraper.db.get_analytics_summary(days=2)
            print(f"\n   • Total engagement: {analytics.get('total_engagement', 0):,}")
            print(f"   • Average sentiment: {analytics.get('avg_sentiment', 0):.2f}")
            print(f"   • Positive tweets: {analytics.get('positive_tweets', 0)}")
            print(f"   • Negative tweets: {analytics.get('negative_tweets', 0)}")
            print(f"   • Neutral tweets: {analytics.get('neutral_tweets', 0)}")
        except Exception as e:
            print(f"   ⚠️  Analytics error: {e}")
    
    scraper.cleanup()
    print("\n👋 Done!\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
