"""
Twitter API v2 Integration
Official API client with rate limiting and advanced features
"""

import time
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from collections import deque

logger = logging.getLogger(__name__)


class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, max_calls: int, time_window: int):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = deque()
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        
        # Remove old calls outside time window
        while self.calls and self.calls[0] < now - self.time_window:
            self.calls.popleft()
        
        # Wait if at limit
        if len(self.calls) >= self.max_calls:
            sleep_time = self.time_window - (now - self.calls[0]) + 1
            if sleep_time > 0:
                logger.info(f"Rate limit reached. Waiting {sleep_time:.1f}s")
                time.sleep(sleep_time)
                self.calls.clear()
        
        self.calls.append(now)


class TwitterAPIClient:
    """Twitter API v2 wrapper with comprehensive features"""
    
    def __init__(self, bearer_token: str = None, **kwargs):
        self.bearer_token = bearer_token
        self.client = None
        self.rate_limiter = RateLimiter(max_calls=450, time_window=900)  # 450 per 15 min
        
        if not bearer_token:
            logger.warning("No bearer token provided. API features disabled.")
            return
        
        try:
            import tweepy
            
            if bearer_token:
                self.client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
                logger.info("Twitter API client initialized")
            else:
                # OAuth 1.0a
                api_key = kwargs.get('api_key')
                api_secret = kwargs.get('api_secret')
                access_token = kwargs.get('access_token')
                access_token_secret = kwargs.get('access_token_secret')
                
                if all([api_key, api_secret, access_token, access_token_secret]):
                    self.client = tweepy.Client(
                        consumer_key=api_key,
                        consumer_secret=api_secret,
                        access_token=access_token,
                        access_token_secret=access_token_secret,
                        wait_on_rate_limit=True
                    )
                    logger.info("Twitter API client initialized with OAuth 1.0a")
                    
        except ImportError:
            logger.error("tweepy not installed. Run: pip install tweepy")
        except Exception as e:
            logger.error(f"Failed to initialize API client: {e}")
    
    def search_recent_tweets(self, query: str, max_results: int = 100, **kwargs) -> List[Dict]:
        """
        Search recent tweets (last 7 days)
        
        Args:
            query: Search query (Twitter search operators)
            max_results: Number of tweets (max 100 per request)
            **kwargs: Additional parameters (start_time, end_time, etc.)
        """
        if not self.client:
            return []
        
        self.rate_limiter.wait_if_needed()
        
        try:
            tweets_data = []
            
            # Paginate if needed
            remaining = max_results
            next_token = None
            
            while remaining > 0:
                batch_size = min(remaining, 100)
                
                response = self.client.search_recent_tweets(
                    query=query,
                    max_results=batch_size,
                    tweet_fields=['created_at', 'public_metrics', 'author_id', 'entities', 'referenced_tweets'],
                    expansions=['author_id', 'referenced_tweets.id'],
                    user_fields=['username', 'name', 'verified', 'public_metrics'],
                    next_token=next_token,
                    **kwargs
                )
                
                if not response.data:
                    break
                
                # Create user map
                users_map = {}
                if response.includes and 'users' in response.includes:
                    for user in response.includes['users']:
                        users_map[user.id] = {
                            'username': user.username,
                            'name': user.name,
                            'verified': getattr(user, 'verified', False)
                        }
                
                # Process tweets
                for tweet in response.data:
                    user_info = users_map.get(tweet.author_id, {})
                    
                    tweet_dict = {
                        'id': str(tweet.id),
                        'text': tweet.text,
                        'created_at': tweet.created_at.isoformat(),
                        'author_id': str(tweet.author_id),
                        'username': user_info.get('username', 'unknown'),
                        'user_name': user_info.get('name', ''),
                        'verified': user_info.get('verified', False),
                        'metrics': {
                            'likes': tweet.public_metrics['like_count'],
                            'retweets': tweet.public_metrics['retweet_count'],
                            'replies': tweet.public_metrics['reply_count'],
                            'quotes': tweet.public_metrics.get('quote_count', 0),
                            'impressions': tweet.public_metrics.get('impression_count', 0)
                        }
                    }
                    
                    # Extract entities
                    if hasattr(tweet, 'entities'):
                        entities = tweet.entities
                        tweet_dict['hashtags'] = [tag['tag'] for tag in entities.get('hashtags', [])]
                        tweet_dict['mentions'] = [m['username'] for m in entities.get('mentions', [])]
                        tweet_dict['urls'] = [url.get('expanded_url', url.get('url', '')) 
                                             for url in entities.get('urls', [])]
                    else:
                        tweet_dict['hashtags'] = []
                        tweet_dict['mentions'] = []
                        tweet_dict['urls'] = []
                    
                    tweets_data.append(tweet_dict)
                
                remaining -= len(response.data)
                
                # Check for next page
                if hasattr(response, 'meta') and 'next_token' in response.meta:
                    next_token = response.meta['next_token']
                    time.sleep(1)  # Rate limiting between pages
                else:
                    break
            
            logger.info(f"Retrieved {len(tweets_data)} tweets for query: {query}")
            return tweets_data
            
        except Exception as e:
            logger.error(f"Error searching tweets: {e}")
            return []
    
    def get_user_tweets(self, username: str = None, user_id: str = None, 
                       max_results: int = 100, **kwargs) -> List[Dict]:
        """Get tweets from a specific user"""
        if not self.client:
            return []
        
        self.rate_limiter.wait_if_needed()
        
        try:
            # Get user ID if username provided
            if username and not user_id:
                user_response = self.client.get_user(username=username)
                if not user_response.data:
                    logger.warning(f"User not found: {username}")
                    return []
                user_id = user_response.data.id
            
            if not user_id:
                return []
            
            tweets_data = []
            next_token = None
            remaining = max_results
            
            while remaining > 0:
                batch_size = min(remaining, 100)
                
                response = self.client.get_users_tweets(
                    id=user_id,
                    max_results=batch_size,
                    tweet_fields=['created_at', 'public_metrics', 'entities', 'referenced_tweets'],
                    pagination_token=next_token,
                    **kwargs
                )
                
                if not response.data:
                    break
                
                for tweet in response.data:
                    tweet_dict = {
                        'id': str(tweet.id),
                        'text': tweet.text,
                        'created_at': tweet.created_at.isoformat(),
                        'username': username,
                        'metrics': {
                            'likes': tweet.public_metrics['like_count'],
                            'retweets': tweet.public_metrics['retweet_count'],
                            'replies': tweet.public_metrics['reply_count']
                        }
                    }
                    
                    # Entities
                    if hasattr(tweet, 'entities'):
                        entities = tweet.entities
                        tweet_dict['hashtags'] = [tag['tag'] for tag in entities.get('hashtags', [])]
                        tweet_dict['mentions'] = [m['username'] for m in entities.get('mentions', [])]
                        tweet_dict['urls'] = [url.get('expanded_url', '') for url in entities.get('urls', [])]
                    
                    tweets_data.append(tweet_dict)
                
                remaining -= len(response.data)
                
                if hasattr(response, 'meta') and 'next_token' in response.meta:
                    next_token = response.meta['next_token']
                else:
                    break
            
            logger.info(f"Retrieved {len(tweets_data)} tweets from @{username}")
            return tweets_data
            
        except Exception as e:
            logger.error(f"Error getting user tweets: {e}")
            return []
    
    def get_user_info(self, username: str) -> Dict:
        """Get detailed user information"""
        if not self.client:
            return {}
        
        self.rate_limiter.wait_if_needed()
        
        try:
            response = self.client.get_user(
                username=username,
                user_fields=['created_at', 'description', 'public_metrics', 'verified', 'location']
            )
            
            if not response.data:
                return {}
            
            user = response.data
            metrics = user.public_metrics
            
            return {
                'id': str(user.id),
                'username': user.username,
                'name': user.name,
                'description': getattr(user, 'description', ''),
                'verified': getattr(user, 'verified', False),
                'location': getattr(user, 'location', ''),
                'created_at': user.created_at.isoformat() if hasattr(user, 'created_at') else None,
                'followers_count': metrics['followers_count'],
                'following_count': metrics['following_count'],
                'tweet_count': metrics['tweet_count'],
                'listed_count': metrics.get('listed_count', 0)
            }
            
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return {}
    
    def search_users(self, query: str, max_results: int = 100) -> List[Dict]:
        """Search for users"""
        # Note: This requires Twitter API v2 with elevated access
        logger.warning("User search requires elevated API access")
        return []
    
    def get_trending_topics(self, woeid: int = 1) -> List[Dict]:
        """Get trending topics (requires API v1.1)"""
        logger.warning("Trending topics require Twitter API v1.1")
        return []


print("API scraper module loaded")
