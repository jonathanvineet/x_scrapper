"""
Example Usage Scripts for Crypto Twitter Intelligence System
"""

import json
import time
from crypto_scraper_orchestrator import CryptoTwitterIntelligence

def load_config(config_file='config.json'):
    """Load configuration from JSON file"""
    with open(config_file, 'r') as f:
        return json.load(f)


def example_1_basic_scraping():
    """Example 1: Basic account scraping"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Account Scraping")
    print("=" * 60)
    
    config = {
        'use_api': False,  # Set to True if you have API credentials
        'use_selenium': True,
        'headless': True,
        'database_path': 'crypto_tweets.db'
    }
    
    scraper = CryptoTwitterIntelligence(config)
    
    try:
        # Scrape specific accounts
        accounts_to_scrape = ['elonmusk', 'VitalikButerin', 'cz_binance']
        
        for account in accounts_to_scrape:
            print(f"\nScraping @{account}...")
            tweets = scraper.scrape_account(account, max_tweets=20)
            print(f"  ✓ Retrieved {len(tweets)} tweets")
            
            # Show sentiment breakdown
            positive = sum(1 for t in tweets if t.sentiment_label == 'positive')
            negative = sum(1 for t in tweets if t.sentiment_label == 'negative')
            neutral = sum(1 for t in tweets if t.sentiment_label == 'neutral')
            
            print(f"  Sentiment: {positive} positive, {negative} negative, {neutral} neutral")
            
            time.sleep(3)  # Rate limiting
        
        print("\n✓ Scraping complete!")
        
    finally:
        scraper.cleanup()


def example_2_keyword_search():
    """Example 2: Keyword-based search"""
    print("=" * 60)
    print("EXAMPLE 2: Keyword Search")
    print("=" * 60)
    
    config = {
        'use_api': False,
        'use_selenium': True,
        'headless': True,
        'database_path': 'crypto_tweets.db'
    }
    
    scraper = CryptoTwitterIntelligence(config)
    
    try:
        # Search for crypto-related keywords
        keywords = ['bitcoin', 'ethereum', '$BTC', '$ETH', 'crypto regulation']
        
        print(f"Searching for {len(keywords)} keywords...")
        tweets = scraper.search_keywords(keywords, max_per_keyword=30)
        
        print(f"\n✓ Found {len(tweets)} unique tweets")
        
        # Analyze top hashtags
        from collections import Counter
        all_hashtags = []
        for tweet in tweets:
            all_hashtags.extend(tweet.hashtags)
        
        top_hashtags = Counter(all_hashtags).most_common(10)
        print("\nTop 10 Hashtags:")
        for tag, count in top_hashtags:
            print(f"  #{tag}: {count} mentions")
        
    finally:
        scraper.cleanup()


def example_3_monitoring():
    """Example 3: Continuous monitoring"""
    print("=" * 60)
    print("EXAMPLE 3: Continuous Monitoring")
    print("=" * 60)
    
    config = {
        'use_api': False,
        'use_selenium': True,
        'headless': True,
        'database_path': 'crypto_tweets.db',
        'monitoring_interval': 300  # 5 minutes
    }
    
    scraper = CryptoTwitterIntelligence(config)
    
    try:
        # Monitor specific categories
        categories = ['crypto_whales', 'trump_ecosystem', 'tech_billionaires']
        
        print(f"Starting monitoring of categories: {', '.join(categories)}")
        print("Press Ctrl+C to stop...")
        print()
        
        # This will run continuously until interrupted
        scraper.monitor_continuous(
            categories=categories,
            interval=300  # Check every 5 minutes
        )
        
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user")
    finally:
        scraper.cleanup()


def example_4_generate_report():
    """Example 4: Generate intelligence report"""
    print("=" * 60)
    print("EXAMPLE 4: Generate Intelligence Report")
    print("=" * 60)
    
    config = {
        'use_api': False,
        'use_selenium': True,
        'headless': True,
        'database_path': 'crypto_tweets.db'
    }
    
    scraper = CryptoTwitterIntelligence(config)
    
    try:
        # Generate report for last 24 hours
        print("Generating intelligence report for last 24 hours...")
        report = scraper.generate_intelligence_report(
            hours=24,
            output_file='crypto_intel_report.json'
        )
        
        print(f"\n✓ Report generated!")
        print(f"  Total tweets analyzed: {report['summary']['total_tweets_analyzed']}")
        print(f"  Unique accounts: {report['summary']['unique_accounts']}")
        print(f"  Total engagement: {report['summary']['total_engagement']:,}")
        
        print(f"\nSentiment Distribution:")
        sentiment = report['sentiment_analysis']
        print(f"  Positive: {sentiment.get('positive', 0)}")
        print(f"  Neutral: {sentiment.get('neutral', 0)}")
        print(f"  Negative: {sentiment.get('negative', 0)}")
        
        print(f"\nTop 5 Trending Hashtags:")
        for i, tag_data in enumerate(report['trending_hashtags'][:5], 1):
            print(f"  {i}. {tag_data['tag']}: {tag_data['mentions']} mentions")
        
        print(f"\nTop 5 Most Active Accounts:")
        for i, account in enumerate(report['most_active_accounts'][:5], 1):
            print(f"  {i}. @{account['username']}: {account['tweets']} tweets, {account['engagement']:,} engagement")
        
    finally:
        scraper.cleanup()


def example_5_comprehensive_workflow():
    """Example 5: Comprehensive workflow"""
    print("=" * 60)
    print("EXAMPLE 5: Comprehensive Intelligence Workflow")
    print("=" * 60)
    
    config = {
        'use_api': False,
        'use_selenium': True,
        'headless': True,
        'database_path': 'crypto_tweets.db'
    }
    
    scraper = CryptoTwitterIntelligence(config)
    
    try:
        # Step 1: Scrape key accounts
        print("\nStep 1: Scraping key crypto influencers...")
        key_accounts = ['elonmusk', 'VitalikButerin', 'brian_armstrong']
        for account in key_accounts:
            tweets = scraper.scrape_account(account, max_tweets=20)
            print(f"  ✓ @{account}: {len(tweets)} tweets")
            time.sleep(3)
        
        # Step 2: Search for trending topics
        print("\nStep 2: Searching trending crypto topics...")
        trending_keywords = ['bitcoin etf', 'ethereum upgrade', 'defi']
        tweets = scraper.search_keywords(trending_keywords, max_per_keyword=20)
        print(f"  ✓ Found {len(tweets)} tweets")
        
        # Step 3: Generate report
        print("\nStep 3: Generating comprehensive report...")
        report = scraper.generate_intelligence_report(
            hours=24,
            output_file='comprehensive_report.json'
        )
        print(f"  ✓ Report saved")
        
        # Step 4: Export data
        print("\nStep 4: Exporting data...")
        scraper.db.export_to_json('tweet_export.json', hours=24)
        print(f"  ✓ Data exported to tweet_export.json")
        
        # Step 5: Display insights
        print("\n" + "=" * 60)
        print("INTELLIGENCE SUMMARY")
        print("=" * 60)
        
        print(f"\nTotal Tweets: {report['summary']['total_tweets_analyzed']}")
        print(f"Unique Accounts: {report['summary']['unique_accounts']}")
        print(f"Total Engagement: {report['summary']['total_engagement']:,}")
        
        if report.get('alerts'):
            print(f"\n⚠️  {len(report['alerts'])} Alerts Generated:")
            for alert in report['alerts']:
                print(f"  • {alert['message']}")
        
        print("\n✓ Complete workflow executed successfully!")
        
    finally:
        scraper.cleanup()


def example_6_api_mode():
    """Example 6: Using Twitter API (requires credentials)"""
    print("=" * 60)
    print("EXAMPLE 6: API-Based Scraping (Faster & More Reliable)")
    print("=" * 60)
    
    # Load credentials from config file
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        if not config.get('use_api') or not config.get('api_credentials', {}).get('bearer_token'):
            print("⚠️  Twitter API credentials not configured in config.json")
            print("   This example requires Twitter API access.")
            print("   See: https://developer.twitter.com/")
            return
        
    except FileNotFoundError:
        print("⚠️  config.json not found. Please create it from config_template.json")
        return
    
    scraper = CryptoTwitterIntelligence(config)
    
    try:
        print("\nUsing Twitter API for faster, more reliable scraping...")
        
        # API can fetch more data faster
        tweets = scraper.scrape_account('VitalikButerin', max_tweets=100)
        print(f"✓ Retrieved {len(tweets)} tweets via API")
        
        # Search is also faster with API
        keywords = ['bitcoin', 'ethereum', 'defi', 'nft']
        search_tweets = scraper.search_keywords(keywords, max_per_keyword=100)
        print(f"✓ Found {len(search_tweets)} tweets via API search")
        
    finally:
        scraper.cleanup()


if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════╗
║   CRYPTO TWITTER INTELLIGENCE - EXAMPLE USAGE SCRIPTS        ║
║   Advanced Twitter Scraper for Web3 & Crypto Intelligence    ║
╚══════════════════════════════════════════════════════════════╝

Choose an example to run:

1. Basic Account Scraping
2. Keyword-Based Search
3. Continuous Monitoring (runs until Ctrl+C)
4. Generate Intelligence Report
5. Comprehensive Workflow
6. API-Based Scraping (requires credentials)
0. Exit

""")
    
    choice = input("Enter choice (0-6): ").strip()
    
    examples = {
        '1': example_1_basic_scraping,
        '2': example_2_keyword_search,
        '3': example_3_monitoring,
        '4': example_4_generate_report,
        '5': example_5_comprehensive_workflow,
        '6': example_6_api_mode
    }
    
    if choice in examples:
        print()
        examples[choice]()
    elif choice == '0':
        print("Goodbye!")
    else:
        print("Invalid choice. Please run again.")
