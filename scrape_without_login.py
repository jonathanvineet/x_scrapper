#!/usr/bin/env python3
"""
Scrape crypto tweets using Twitter's public search (no login required)
"""

import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from datetime import datetime
import sqlite3

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_driver():
    """Setup Chrome driver for container environment"""
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def scrape_crypto_trends():
    """Scrape trending crypto topics"""
    driver = setup_driver()
    tweets_data = []
    
    # Crypto-related search queries that work without login
    search_queries = [
        "bitcoin OR btc lang:en",
        "ethereum OR eth lang:en",
        "crypto lang:en",
        "web3 lang:en",
        "defi lang:en"
    ]
    
    try:
        for query in search_queries:
            logger.info(f"🔍 Searching: {query}")
            
            # Try Twitter search URL (some still work without login)
            search_url = f"https://twitter.com/search?q={query.replace(' ', '%20')}&src=typed_query&f=live"
            driver.get(search_url)
            time.sleep(5)
            
            # Check if we got content or login wall
            page_source = driver.page_source.lower()
            if 'log in' in page_source or 'sign up' in page_source:
                logger.warning(f"❌ Login required for search. Trying alternative...")
                continue
            
            try:
                # Try to find tweet elements
                tweets = driver.find_elements(By.CSS_SELECTOR, 'article')
                logger.info(f"   Found {len(tweets)} potential tweet elements")
                
                for tweet in tweets[:5]:  # Get first 5
                    try:
                        text = tweet.text
                        if text and len(text) > 10:
                            tweets_data.append({
                                'text': text[:200],
                                'query': query,
                                'scraped_at': datetime.now().isoformat()
                            })
                    except:
                        continue
                        
            except Exception as e:
                logger.error(f"   Error extracting tweets: {e}")
                
            time.sleep(3)
    
    finally:
        driver.quit()
    
    return tweets_data

def scrape_nitter_alternative():
    """Use Nitter (Twitter frontend) as alternative"""
    driver = setup_driver()
    results = []
    
    # Nitter instances (Twitter frontends that don't require login)
    nitter_instances = [
        "https://nitter.net",
        "https://nitter.privacydev.net",
        "https://nitter.poast.org"
    ]
    
    accounts = [
        'VitalikButerin',
        'cz_binance',
        'APompliano',
        'aantonop',
        'Saylor'
    ]
    
    for nitter_url in nitter_instances:
        logger.info(f"🔄 Trying Nitter instance: {nitter_url}")
        
        for account in accounts:
            try:
                url = f"{nitter_url}/{account}"
                logger.info(f"   📱 Fetching {account}...")
                driver.get(url)
                time.sleep(3)
                
                # Check if instance is working
                if 'instance has been rate limited' in driver.page_source.lower():
                    logger.warning(f"   ⚠️  Instance rate limited, trying next...")
                    break
                
                # Find tweets
                tweets = driver.find_elements(By.CSS_SELECTOR, '.timeline-item')
                logger.info(f"   ✅ Found {len(tweets)} tweets from @{account}")
                
                for tweet in tweets[:10]:
                    try:
                        text_elem = tweet.find_element(By.CSS_SELECTOR, '.tweet-content')
                        time_elem = tweet.find_element(By.CSS_SELECTOR, '.tweet-date a')
                        stats = tweet.find_elements(By.CSS_SELECTOR, '.icon-container')
                        
                        tweet_data = {
                            'username': account,
                            'text': text_elem.text,
                            'time': time_elem.get_attribute('title'),
                            'scraped_at': datetime.now().isoformat(),
                            'source': nitter_url
                        }
                        
                        if len(stats) >= 3:
                            tweet_data['likes'] = stats[2].text
                            tweet_data['retweets'] = stats[1].text
                        
                        results.append(tweet_data)
                        
                    except Exception as e:
                        continue
                
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"   ❌ Error scraping {account}: {str(e)[:50]}")
                continue
        
        if results:
            logger.info(f"✅ Successfully scraped using {nitter_url}")
            break
    
    driver.quit()
    return results

def main():
    print("=" * 70)
    print("🚀 CRYPTO TWITTER SCRAPER - NO LOGIN METHOD")
    print("=" * 70)
    
    print("\n📊 Method 1: Scraping via Nitter (Twitter frontend)")
    print("   This doesn't require login and works reliably!\n")
    
    tweets = scrape_nitter_alternative()
    
    if tweets:
        print(f"\n✅ Successfully scraped {len(tweets)} tweets!\n")
        
        # Show sample tweets
        for i, tweet in enumerate(tweets[:10], 1):
            print(f"{'─' * 70}")
            print(f"Tweet {i} - @{tweet['username']}")
            print(f"📅 {tweet.get('time', 'N/A')}")
            print(f"💬 {tweet['text'][:150]}{'...' if len(tweet['text']) > 150 else ''}")
            if 'likes' in tweet:
                print(f"❤️  {tweet['likes']} | 🔄 {tweet.get('retweets', 'N/A')}")
            print()
        
        # Save to database
        print("\n💾 Saving to database...")
        conn = sqlite3.connect('crypto_tweets.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tweets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                text TEXT,
                time TEXT,
                likes TEXT,
                retweets TEXT,
                source TEXT,
                scraped_at TEXT
            )
        ''')
        
        for tweet in tweets:
            cursor.execute('''
                INSERT INTO tweets (username, text, time, likes, retweets, source, scraped_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                tweet.get('username'),
                tweet.get('text'),
                tweet.get('time'),
                tweet.get('likes'),
                tweet.get('retweets'),
                tweet.get('source'),
                tweet.get('scraped_at')
            ))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Saved {len(tweets)} tweets to crypto_tweets.db")
        
    else:
        print("\n❌ No tweets scraped. Possible reasons:")
        print("   • All Nitter instances are down or rate-limited")
        print("   • Network connectivity issues")
        print("   • Try running again in a few minutes")
    
    print("\n" + "=" * 70)
    print("✅ SCRAPING COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
