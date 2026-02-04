"""
Advanced Twitter/X Scraper for Web3, Crypto & Stock Market Intelligence
Main orchestration module
"""

import json
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import sqlite3
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class Tweet:
    """Enhanced tweet data structure"""
    tweet_id: str
    username: str
    display_name: str
    text: str
    timestamp: datetime
    likes: int
    retweets: int
    replies: int
    views: Optional[int]
    is_verified: bool
    hashtags: List[str]
    mentions: List[str]
    urls: List[str]
    media_urls: List[str]
    sentiment_score: Optional[float]
    sentiment_label: Optional[str]
    scraped_at: datetime
    source: str
    
    def to_dict(self):
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        data['scraped_at'] = self.scraped_at.isoformat()
        return data


class SentimentAnalyzer:
    """Advanced sentiment analysis with crypto-specific vocabulary"""
    
    def __init__(self):
        self.crypto_positive = {
            'bullish', 'moon', 'rocket', 'pump', 'gains', 'breakthrough',
            'adoption', 'partnership', 'launch', 'approved', 'soaring', 'surge',
            'rally', 'breakout', 'accumulate', 'hodl', 'gem', 'alpha', 'long',
            'buy', 'accumulation', 'institutional', 'etf', 'utility', 'adoption'
        }
        
        self.crypto_negative = {
            'bearish', 'dump', 'crash', 'scam', 'rug', 'rugpull', 'fud',
            'decline', 'plunge', 'reject', 'rejected', 'liquidation', 'short',
            'hack', 'exploit', 'vulnerable', 'warning', 'caution', 'ponzi',
            'bubble', 'overvalued', 'sell', 'exit', 'risk', 'fraud'
        }
        
        self.market_indicators = {
            'positive': ['ath', 'breakout', 'golden cross', 'support', 'buy signal'],
            'negative': ['death cross', 'resistance', 'sell signal', 'breakdown']
        }
    
    def analyze(self, text: str) -> Dict:
        """Comprehensive sentiment analysis"""
        text_lower = text.lower()
        words = set(text_lower.split())
        
        # Count keyword matches
        positive_matches = len(words.intersection(self.crypto_positive))
        negative_matches = len(words.intersection(self.crypto_negative))
        
        # Pattern matching for phrases
        positive_patterns = sum(1 for phrase in self.market_indicators['positive'] 
                               if phrase in text_lower)
        negative_patterns = sum(1 for phrase in self.market_indicators['negative'] 
                               if phrase in text_lower)
        
        # Calculate score
        total_signals = positive_matches + negative_matches + positive_patterns + negative_patterns
        if total_signals == 0:
            polarity = 0.0
        else:
            polarity = ((positive_matches + positive_patterns) - 
                       (negative_matches + negative_patterns)) / total_signals
        
        # Emoji analysis
        bullish_emojis = text.count('🚀') + text.count('📈') + text.count('💎') + text.count('🐂')
        bearish_emojis = text.count('📉') + text.count('🐻') + text.count('💀')
        
        polarity += (bullish_emojis - bearish_emojis) * 0.05
        polarity = max(-1.0, min(1.0, polarity))
        
        # Determine label
        if polarity > 0.15:
            label = "positive"
        elif polarity < -0.15:
            label = "negative"
        else:
            label = "neutral"
        
        return {
            'polarity': polarity,
            'label': label,
            'positive_signals': positive_matches + positive_patterns,
            'negative_signals': negative_matches + negative_patterns,
            'confidence': abs(polarity)
        }


class DataPersistence:
    """Advanced database management with analytics"""
    
    def __init__(self, db_path: str = "crypto_twitter.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_database()
    
    def _init_database(self):
        """Create comprehensive database schema"""
        cursor = self.conn.cursor()
        
        # Main tweets table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tweets (
                tweet_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                display_name TEXT,
                text TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                likes INTEGER DEFAULT 0,
                retweets INTEGER DEFAULT 0,
                replies INTEGER DEFAULT 0,
                views INTEGER,
                is_verified BOOLEAN DEFAULT 0,
                hashtags TEXT,
                mentions TEXT,
                urls TEXT,
                media_urls TEXT,
                sentiment_score REAL,
                sentiment_label TEXT,
                scraped_at TEXT NOT NULL,
                source TEXT NOT NULL
            )
        ''')
        
        # Analytics table for aggregated metrics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_analytics (
                date TEXT PRIMARY KEY,
                total_tweets INTEGER,
                total_engagement INTEGER,
                avg_sentiment REAL,
                trending_topics TEXT,
                top_accounts TEXT,
                created_at TEXT
            )
        ''')
        
        # Monitored accounts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monitored_accounts (
                username TEXT PRIMARY KEY,
                category TEXT,
                follower_count INTEGER,
                last_checked TEXT,
                added_at TEXT
            )
        ''')
        
        # Keywords tracking
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracked_keywords (
                keyword TEXT PRIMARY KEY,
                category TEXT,
                mention_count INTEGER DEFAULT 0,
                avg_sentiment REAL,
                last_updated TEXT
            )
        ''')
        
        # Create indices for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_username ON tweets(username)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON tweets(timestamp)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_sentiment ON tweets(sentiment_label)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_scraped_at ON tweets(scraped_at)')
        
        self.conn.commit()
        logger.info("Database initialized successfully")
    
    def save_tweet(self, tweet: Tweet):
        """Save tweet with conflict handling"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO tweets VALUES 
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tweet.tweet_id,
                tweet.username,
                tweet.display_name,
                tweet.text,
                tweet.timestamp.isoformat(),
                tweet.likes,
                tweet.retweets,
                tweet.replies,
                tweet.views,
                tweet.is_verified,
                json.dumps(tweet.hashtags),
                json.dumps(tweet.mentions),
                json.dumps(tweet.urls),
                json.dumps(tweet.media_urls),
                tweet.sentiment_score,
                tweet.sentiment_label,
                tweet.scraped_at.isoformat(),
                tweet.source
            ))
            
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error saving tweet: {e}")
            return False
    
    def get_tweets(self, filters: Dict = None, limit: int = 100) -> List[Dict]:
        """Flexible tweet retrieval with filtering"""
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM tweets WHERE 1=1"
        params = []
        
        if filters:
            if 'username' in filters:
                query += " AND username = ?"
                params.append(filters['username'])
            
            if 'since' in filters:
                query += " AND timestamp >= ?"
                params.append(filters['since'])
            
            if 'sentiment' in filters:
                query += " AND sentiment_label = ?"
                params.append(filters['sentiment'])
            
            if 'min_engagement' in filters:
                query += " AND (likes + retweets) >= ?"
                params.append(filters['min_engagement'])
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        return self._rows_to_dicts(cursor.fetchall())
    
    def get_trending_analysis(self, hours: int = 24) -> Dict:
        """Generate trending analysis"""
        cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
        cursor = self.conn.cursor()
        
        # Get all recent tweets
        cursor.execute('''
            SELECT text, sentiment_label, likes, retweets, hashtags, username
            FROM tweets WHERE timestamp > ?
        ''', (cutoff,))
        
        tweets = cursor.fetchall()
        
        # Analyze hashtags
        hashtag_counts = defaultdict(int)
        hashtag_engagement = defaultdict(int)
        
        # Analyze accounts
        account_stats = defaultdict(lambda: {'tweets': 0, 'engagement': 0})
        
        # Sentiment distribution
        sentiment_counts = defaultdict(int)
        
        for text, sentiment, likes, retweets, hashtags_json, username in tweets:
            # Process hashtags
            try:
                hashtags = json.loads(hashtags_json)
                for tag in hashtags:
                    hashtag_counts[tag] += 1
                    hashtag_engagement[tag] += likes + retweets
            except:
                pass
            
            # Process accounts
            account_stats[username]['tweets'] += 1
            account_stats[username]['engagement'] += likes + retweets
            
            # Process sentiment
            sentiment_counts[sentiment or 'neutral'] += 1
        
        # Get top hashtags
        top_hashtags = sorted(
            [(tag, count, hashtag_engagement[tag]) 
             for tag, count in hashtag_counts.items()],
            key=lambda x: x[2],
            reverse=True
        )[:20]
        
        # Get top accounts
        top_accounts = sorted(
            [(user, stats['tweets'], stats['engagement']) 
             for user, stats in account_stats.items()],
            key=lambda x: x[2],
            reverse=True
        )[:15]
        
        return {
            'total_tweets': len(tweets),
            'sentiment_breakdown': dict(sentiment_counts),
            'top_hashtags': [
                {'tag': tag, 'mentions': count, 'engagement': eng}
                for tag, count, eng in top_hashtags
            ],
            'top_accounts': [
                {'username': user, 'tweets': tweets, 'engagement': eng}
                for user, tweets, eng in top_accounts
            ]
        }
    
    def _rows_to_dicts(self, rows) -> List[Dict]:
        """Convert database rows to dictionaries"""
        columns = [
            'tweet_id', 'username', 'display_name', 'text', 'timestamp',
            'likes', 'retweets', 'replies', 'views', 'is_verified',
            'hashtags', 'mentions', 'urls', 'media_urls',
            'sentiment_score', 'sentiment_label', 'scraped_at', 'source'
        ]
        
        results = []
        for row in rows:
            tweet_dict = dict(zip(columns, row))
            # Parse JSON fields
            for field in ['hashtags', 'mentions', 'urls', 'media_urls']:
                try:
                    tweet_dict[field] = json.loads(tweet_dict[field])
                except:
                    tweet_dict[field] = []
            results.append(tweet_dict)
        
        return results
    
    def export_to_json(self, filename: str, hours: int = 24):
        """Export data to JSON"""
        tweets = self.get_tweets(
            filters={'since': (datetime.now() - timedelta(hours=hours)).isoformat()},
            limit=10000
        )
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(tweets, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(tweets)} tweets to {filename}")
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()


print("Scraper main module loaded successfully")
