"""
Main Orchestrator for Crypto Twitter Intelligence System
Coordinates all scraping, analysis, and reporting
"""

import json
import time
import logging
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

# Import our modules
from scraper_main import Tweet, SentimentAnalyzer, DataPersistence
from selenium_scraper import SeleniumTwitterScraper
from api_scraper import TwitterAPIClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crypto_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class CryptoTwitterIntelligence:
    """
    Main orchestrator for comprehensive crypto Twitter intelligence
    """
    
    # Comprehensive account lists
    MONITORED_ACCOUNTS = {
        'crypto_whales': [
            'elonmusk', 'VitalikButerin', 'cz_binance', 'brian_armstrong',
            'APompliano', 'naval', 'balajis', 'aantonop', 'Saylor Michael',
            'novogratz', 'CathieDWood', 'RaoulGMI'
        ],
        'trump_ecosystem': [
            'realDonaldTrump', 'DonaldJTrumpJr', 'EricTrump', 'IvankaTrump',
            'LaraLeaTrump'
        ],
        'tech_billionaires': [
            'elonmusk', 'BillGates', 'jeffbezos', 'MarkZuckerberg',
            'sundarpichai', 'tim_cook', 'satyanadella'
        ],
        'crypto_founders': [
            'VitalikButerin', 'justinsuntron', 'hoskinson_charles',
            'aantonop', 'stani_kulechov', 'haydenzadams'
        ],
        'crypto_media': [
            'CoinDesk', 'Cointelegraph', 'Crypto', 'TheCryptoLark',
            'Crypto', 'bitcoinmagazine', 'Decrypt media', 'TheBlockPro'
        ],
        'defi_protocols': [
            'Uniswap', 'AaveAave', 'CurveFinance', 'MakerDAO',
            'Compound', 'synthetix_io', 'SushiSwap', 'yearn'
        ],
        'nft_ecosystem': [
            'opensea', 'yugalabs', 'proof_xyz', 'pudgypenguins',
            'azuki', 'doodles', 'worldofwomennft'
        ],
        'venture_capital': [
            'a16zcrypto', 'Paradigm', 'dragonfly_cap', 'Polychain Capital',
            'Pantera', 'coinbase ventures'
        ],
        'exchanges': [
            'binance', 'coinbase', 'krakenfx', 'Gemini', 'okx'
        ],
        'analysts': [
            'DocumentingBTC', 'WClementeIII', 'woonomic', 'glassnode',
            'santimentfeed', 'CryptoQuant_com'
        ]
    }
    
    # Comprehensive keyword tracking
    TRACKED_KEYWORDS = {
        'major_cryptos': [
            'bitcoin', 'btc', '$btc', 'ethereum', 'eth', '$eth',
            'solana', 'sol', '$sol', 'cardano', 'ada', 'xrp', 'ripple',
            'bnb', 'binance coin', 'dogecoin', 'doge', 'polygon', 'matic',
            'avalanche', 'avax', 'polkadot', 'dot', 'chainlink', 'link'
        ],
        'defi': [
            'defi', 'decentralized finance', 'yield farming', 'liquidity pool',
            'amm', 'dex', 'lending protocol', 'stablecoin', 'usdt', 'usdc',
            'dai', 'liquidity mining', 'tvl', 'total value locked'
        ],
        'nft': [
            'nft', 'non-fungible', 'opensea', 'blur', 'pfp', 'generative art',
            'digital collectible', 'mint', 'floor price', 'blue chip nft'
        ],
        'market_sentiment': [
            'bullish', 'bearish', 'moon', 'dump', 'pump', 'fomo', 'fud',
            'hodl', 'diamond hands', 'paper hands', 'rekt', 'ape in',
            'to the moon', '🚀', '📈', '📉', 'bull run', 'bear market',
            'alt season', 'btc dominance'
        ],
        'technical_analysis': [
            'support level', 'resistance', 'breakout', 'breakdown', 'head and shoulders',
            'bull flag', 'bear flag', 'golden cross', 'death cross',
            'rsi', 'macd', 'fibonacci', 'elliott wave', 'wyckoff'
        ],
        'regulation': [
            'sec', 'securities and exchange', 'regulatory', 'compliance',
            'etf approval', 'bitcoin etf', 'crypto regulation', 'cftc',
            'cbdc', 'central bank digital currency', 'lawsuit', 'settlement'
        ],
        'trump_crypto': [
            'trump coin', 'trump token', 'truth social', 'trump nft',
            'maga coin', 'trump + crypto', 'trump + bitcoin'
        ],
        'musk_crypto': [
            'dogecoin', 'doge', 'twitter payments', 'x payments',
            'musk + crypto', 'tesla + bitcoin'
        ],
        'tech_stocks': [
            '$aapl', 'apple stock', '$tsla', 'tesla stock', '$googl', 'google stock',
            '$msft', 'microsoft stock', '$amzn', 'amazon stock', '$meta', 'meta stock',
            '$nvda', 'nvidia stock', 'sp500', 'nasdaq', 'dow jones'
        ],
        'market_events': [
            'halving', 'hard fork', 'mainnet launch', 'testnet',
            'airdrop', 'token unlock', 'vesting', 'partnership announcement',
            'acquisition', 'listing', 'delisting', 'hack', 'exploit'
        ],
        'institutional': [
            'institutional adoption', 'blackrock', 'fidelity', 'goldman sachs',
            'jpmorgan', 'wall street', 'traditional finance', 'tradfi',
            'pension fund', 'sovereign wealth'
        ]
    }
    
    def __init__(self, config: Dict):
        """
        Initialize the intelligence system
        
        Config should contain:
        - use_api: bool
        - api_credentials: dict (if use_api=True)
        - use_selenium: bool
        - headless: bool
        - proxy: str (optional)
        - database_path: str
        - monitoring_interval: int (seconds)
        """
        self.config = config
        
        # Initialize components
        self.api_client = None
        if config.get('use_api') and config.get('api_credentials'):
            self.api_client = TwitterAPIClient(**config['api_credentials'])
        
        self.selenium_scraper = None
        if config.get('use_selenium', True):
            self.selenium_scraper = SeleniumTwitterScraper(
                headless=config.get('headless', True),
                proxy=config.get('proxy')
            )
        
        self.sentiment_analyzer = SentimentAnalyzer()
        self.db = DataPersistence(config.get('database_path', 'crypto_intelligence.db'))
        
        self.is_monitoring = False
        self.monitoring_thread = None
        
        logger.info("Crypto Twitter Intelligence System initialized")
    
    def scrape_account(self, username: str, max_tweets: int = 50, force_selenium: bool = False) -> List[Tweet]:
        """Scrape tweets from a specific account using best available method"""
        logger.info(f"Scraping @{username}...")
        
        tweets = []
        
        # Try API first (if available and not forced to Selenium)
        if self.api_client and not force_selenium:
            try:
                api_data = self.api_client.get_user_tweets(username=username, max_results=max_tweets)
                tweets.extend(self._process_api_data(api_data))
                logger.info(f"Retrieved {len(tweets)} tweets via API")
            except Exception as e:
                logger.error(f"API scraping failed for @{username}: {e}")
        
        # Fall back to or use Selenium
        if (len(tweets) < max_tweets or force_selenium) and self.selenium_scraper:
            try:
                selenium_data = self.selenium_scraper.scrape_user_timeline(username, max_tweets)
                additional_tweets = self._process_selenium_data(selenium_data)
                tweets.extend(additional_tweets)
                logger.info(f"Retrieved {len(additional_tweets)} tweets via Selenium")
            except Exception as e:
                logger.error(f"Selenium scraping failed for @{username}: {e}")
        
        # Save to database
        for tweet in tweets:
            self.db.save_tweet(tweet)
        
        return tweets
    
    def search_keywords(self, keywords: List[str], max_per_keyword: int = 50) -> List[Tweet]:
        """Search for tweets containing keywords"""
        all_tweets = []
        seen_ids = set()
        
        for keyword in keywords:
            logger.info(f"Searching: {keyword}")
            
            # Try API first
            if self.api_client:
                try:
                    query = f"{keyword} -is:retweet lang:en"
                    api_data = self.api_client.search_recent_tweets(query, max_results=max_per_keyword)
                    tweets = self._process_api_data(api_data)
                    
                    for tweet in tweets:
                        if tweet.tweet_id not in seen_ids:
                            seen_ids.add(tweet.tweet_id)
                            all_tweets.append(tweet)
                            self.db.save_tweet(tweet)
                except Exception as e:
                    logger.error(f"API search failed for '{keyword}': {e}")
            
            # Try Selenium
            if self.selenium_scraper and len(all_tweets) < max_per_keyword * len(keywords):
                try:
                    selenium_data = self.selenium_scraper.search_tweets(keyword, max_per_keyword)
                    tweets = self._process_selenium_data(selenium_data)
                    
                    for tweet in tweets:
                        if tweet.tweet_id not in seen_ids:
                            seen_ids.add(tweet.tweet_id)
                            all_tweets.append(tweet)
                            self.db.save_tweet(tweet)
                except Exception as e:
                    logger.error(f"Selenium search failed for '{keyword}': {e}")
            
            time.sleep(2)  # Rate limiting
        
        logger.info(f"Total tweets found: {len(all_tweets)}")
        return all_tweets
    
    def monitor_continuous(self, categories: List[str] = None, interval: int = 300):
        """
        Start continuous monitoring of accounts
        
        Args:
            categories: Account categories to monitor (default: all)
            interval: Check interval in seconds (default: 5 minutes)
        """
        if categories is None:
            categories = list(self.MONITORED_ACCOUNTS.keys())
        
        accounts = []
        for category in categories:
            if category in self.MONITORED_ACCOUNTS:
                accounts.extend(self.MONITORED_ACCOUNTS[category])
        
        accounts = list(set(accounts))  # Remove duplicates
        
        logger.info(f"Starting continuous monitoring of {len(accounts)} accounts")
        logger.info(f"Categories: {', '.join(categories)}")
        logger.info(f"Check interval: {interval}s")
        
        self.is_monitoring = True
        
        try:
            while self.is_monitoring:
                cycle_start = time.time()
                
                for username in accounts:
                    if not self.is_monitoring:
                        break
                    
                    try:
                        tweets = self.scrape_account(username, max_tweets=10)
                        logger.info(f"@{username}: {len(tweets)} tweets")
                        time.sleep(5)  # Rate limiting between accounts
                    except Exception as e:
                        logger.error(f"Error monitoring @{username}: {e}")
                
                # Wait for next cycle
                cycle_time = time.time() - cycle_start
                wait_time = max(0, interval - cycle_time)
                
                if wait_time > 0 and self.is_monitoring:
                    logger.info(f"Cycle complete. Waiting {wait_time:.0f}s until next check...")
                    time.sleep(wait_time)
                    
        except KeyboardInterrupt:
            logger.info("Monitoring stopped by user")
        finally:
            self.is_monitoring = False
    
    def start_background_monitoring(self, categories: List[str] = None, interval: int = 300):
        """Start monitoring in background thread"""
        if self.monitoring_thread and self.monitoring_thread.is_alive():
            logger.warning("Monitoring already running")
            return
        
        self.monitoring_thread = threading.Thread(
            target=self.monitor_continuous,
            args=(categories, interval),
            daemon=True
        )
        self.monitoring_thread.start()
        logger.info("Background monitoring started")
    
    def stop_monitoring(self):
        """Stop background monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=10)
        logger.info("Monitoring stopped")
    
    def generate_intelligence_report(self, hours: int = 24, output_file: str = None) -> Dict:
        """Generate comprehensive intelligence report"""
        logger.info(f"Generating intelligence report for last {hours} hours...")
        
        # Get trending analysis
        analysis = self.db.get_trending_analysis(hours=hours)
        
        # Get tweets for detailed analysis
        since = (datetime.now() - timedelta(hours=hours)).isoformat()
        tweets = self.db.get_tweets(filters={'since': since}, limit=10000)
        
        # Compile report
        report = {
            'generated_at': datetime.now().isoformat(),
            'time_period_hours': hours,
            'summary': {
                'total_tweets_analyzed': analysis['total_tweets'],
                'unique_accounts': len(set(t['username'] for t in tweets)),
                'total_engagement': sum(t['likes'] + t['retweets'] for t in tweets)
            },
            'sentiment_analysis': analysis['sentiment_breakdown'],
            'trending_hashtags': analysis['top_hashtags'][:25],
            'most_active_accounts': analysis['top_accounts'][:20],
            'top_tweets_by_engagement': sorted(
                tweets,
                key=lambda t: t['likes'] + t['retweets'] * 2,
                reverse=True
            )[:30],
            'alerts': self._generate_alerts(tweets),
            'keyword_mentions': self._analyze_keyword_mentions(tweets)
        }
        
        # Save report
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"intelligence_report_{timestamp}.json"
        
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Report saved to: {output_path}")
        return report
    
    def _process_api_data(self, api_data: List[Dict]) -> List[Tweet]:
        """Convert API data to Tweet objects"""
        tweets = []
        
        for data in api_data:
            sentiment = self.sentiment_analyzer.analyze(data['text'])
            
            tweet = Tweet(
                tweet_id=data['id'],
                username=data.get('username', 'unknown'),
                display_name=data.get('user_name', ''),
                text=data['text'],
                timestamp=datetime.fromisoformat(data['created_at'].replace('Z', '+00:00')),
                likes=data['metrics'].get('likes', 0),
                retweets=data['metrics'].get('retweets', 0),
                replies=data['metrics'].get('replies', 0),
                views=data['metrics'].get('impressions'),
                is_verified=data.get('verified', False),
                hashtags=data.get('hashtags', []),
                mentions=data.get('mentions', []),
                urls=data.get('urls', []),
                media_urls=[],
                sentiment_score=sentiment['polarity'],
                sentiment_label=sentiment['label'],
                scraped_at=datetime.now(),
                source='api'
            )
            
            tweets.append(tweet)
        
        return tweets
    
    def _process_selenium_data(self, selenium_data: List[Dict]) -> List[Tweet]:
        """Convert Selenium data to Tweet objects"""
        tweets = []
        
        for data in selenium_data:
            sentiment = self.sentiment_analyzer.analyze(data['text'])
            
            timestamp_str = data.get('timestamp')
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            except:
                timestamp = datetime.now()
            
            metrics = data.get('metrics', {})
            
            tweet = Tweet(
                tweet_id=data['id'],
                username=data.get('username', 'unknown'),
                display_name=data.get('username', ''),
                text=data['text'],
                timestamp=timestamp,
                likes=metrics.get('likes', 0),
                retweets=metrics.get('retweets', 0),
                replies=metrics.get('replies', 0),
                views=metrics.get('views'),
                is_verified=False,
                hashtags=data.get('hashtags', []),
                mentions=data.get('mentions', []),
                urls=data.get('urls', []),
                media_urls=[],
                sentiment_score=sentiment['polarity'],
                sentiment_label=sentiment['label'],
                scraped_at=datetime.now(),
                source='selenium'
            )
            
            tweets.append(tweet)
        
        return tweets
    
    def _generate_alerts(self, tweets: List[Dict]) -> List[Dict]:
        """Generate alerts for significant events"""
        alerts = []
        
        # High engagement tweets
        high_engagement = [t for t in tweets if (t['likes'] + t['retweets']) > 10000]
        if high_engagement:
            alerts.append({
                'type': 'high_engagement',
                'count': len(high_engagement),
                'message': f"{len(high_engagement)} tweets with >10K engagement",
                'examples': high_engagement[:5]
            })
        
        # Sentiment spikes
        very_positive = [t for t in tweets if t.get('sentiment_score', 0) > 0.5]
        very_negative = [t for t in tweets if t.get('sentiment_score', 0) < -0.5]
        
        if very_positive:
            alerts.append({
                'type': 'positive_sentiment_spike',
                'count': len(very_positive),
                'message': f"{len(very_positive)} very positive tweets detected"
            })
        
        if very_negative:
            alerts.append({
                'type': 'negative_sentiment_spike',
                'count': len(very_negative),
                'message': f"{len(very_negative)} very negative tweets detected"
            })
        
        return alerts
    
    def _analyze_keyword_mentions(self, tweets: List[Dict]) -> Dict:
        """Analyze keyword mentions"""
        keyword_stats = {}
        
        for category, keywords in self.TRACKED_KEYWORDS.items():
            mentions = 0
            avg_sentiment = 0
            sentiment_scores = []
            
            for tweet in tweets:
                text_lower = tweet['text'].lower()
                for keyword in keywords:
                    if keyword.lower() in text_lower:
                        mentions += 1
                        if tweet.get('sentiment_score') is not None:
                            sentiment_scores.append(tweet['sentiment_score'])
                        break
            
            if sentiment_scores:
                avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
            
            keyword_stats[category] = {
                'mentions': mentions,
                'avg_sentiment': avg_sentiment
            }
        
        return keyword_stats
    
    def cleanup(self):
        """Cleanup resources"""
        self.stop_monitoring()
        
        if self.selenium_scraper:
            self.selenium_scraper.close()
        
        if self.db:
            self.db.close()
        
        logger.info("Cleanup complete")


print("Orchestrator module loaded successfully")
