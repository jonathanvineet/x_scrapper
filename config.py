"""
Configuration management with environment variable support
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class that reads from environment variables"""
    
    # API Credentials
    X_CONSUMER_KEY = os.getenv('X_CONSUMER_KEY', '')
    X_SECRET_KEY = os.getenv('X_SECRET_KEY', '')
    X_BEARER_TOKEN = os.getenv('X_BEARER_TOKEN', '')
    X_ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN', '')
    X_ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET', '')
    
    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'crypto_intelligence.db')
    
    # Scraping Configuration
    USE_API = os.getenv('USE_API', 'false').lower() == 'true'
    USE_SELENIUM = os.getenv('USE_SELENIUM', 'true').lower() == 'true'
    HEADLESS = os.getenv('HEADLESS', 'true').lower() == 'true'
    PROXY = os.getenv('PROXY', None)
    MONITORING_INTERVAL = int(os.getenv('MONITORING_INTERVAL', '300'))
    
    # Scraping Limits
    MAX_TWEETS_PER_ACCOUNT = int(os.getenv('MAX_TWEETS_PER_ACCOUNT', '50'))
    MAX_TWEETS_PER_KEYWORD = int(os.getenv('MAX_TWEETS_PER_KEYWORD', '100'))
    SCROLL_PAUSE_TIME = float(os.getenv('SCROLL_PAUSE_TIME', '2.0'))
    RATE_LIMIT_DELAY = int(os.getenv('RATE_LIMIT_DELAY', '5'))
    
    # Alerts
    HIGH_ENGAGEMENT_THRESHOLD = int(os.getenv('HIGH_ENGAGEMENT_THRESHOLD', '10000'))
    SENTIMENT_THRESHOLD = float(os.getenv('SENTIMENT_THRESHOLD', '0.5'))
    ENABLE_EMAIL_ALERTS = os.getenv('ENABLE_EMAIL_ALERTS', 'false').lower() == 'true'
    
    # Export
    AUTO_EXPORT = os.getenv('AUTO_EXPORT', 'true').lower() == 'true'
    EXPORT_INTERVAL_HOURS = int(os.getenv('EXPORT_INTERVAL_HOURS', '24'))
    EXPORT_FORMATS = os.getenv('EXPORT_FORMATS', 'json,csv').split(',')
    EXPORT_DIRECTORY = os.getenv('EXPORT_DIRECTORY', './exports')
    
    @classmethod
    def get_api_credentials(cls) -> dict:
        """Get API credentials as dictionary"""
        return {
            'consumer_key': cls.X_CONSUMER_KEY,
            'secret_key': cls.X_SECRET_KEY,
            'bearer_token': cls.X_BEARER_TOKEN,
            'access_token': cls.X_ACCESS_TOKEN,
            'access_token_secret': cls.X_ACCESS_TOKEN_SECRET,
        }
    
    @classmethod
    def validate_credentials(cls) -> bool:
        """Validate that required credentials are set"""
        required_fields = {
            'X_CONSUMER_KEY': cls.X_CONSUMER_KEY,
            'X_SECRET_KEY': cls.X_SECRET_KEY,
            'X_BEARER_TOKEN': cls.X_BEARER_TOKEN,
        }
        
        missing = [key for key, value in required_fields.items() if not value]
        
        if missing:
            print(f"❌ Missing credentials: {', '.join(missing)}")
            print("📝 Please set these in your .env file")
            return False
        
        return True
    
    @classmethod
    def print_config(cls):
        """Print non-sensitive configuration"""
        print("\n=== Current Configuration ===")
        print(f"📊 USE_API: {cls.USE_API}")
        print(f"🌐 USE_SELENIUM: {cls.USE_SELENIUM}")
        print(f"🤫 HEADLESS: {cls.HEADLESS}")
        print(f"💾 DATABASE: {cls.DATABASE_PATH}")
        print(f"📈 MAX_TWEETS_PER_ACCOUNT: {cls.MAX_TWEETS_PER_ACCOUNT}")
        print(f"🔍 MAX_TWEETS_PER_KEYWORD: {cls.MAX_TWEETS_PER_KEYWORD}")
        print(f"⏱️  MONITORING_INTERVAL: {cls.MONITORING_INTERVAL}s")
        print(f"📤 AUTO_EXPORT: {cls.AUTO_EXPORT}")
        print(f"✅ API Credentials configured: {cls.validate_credentials()}")
        print("=" * 30 + "\n")


if __name__ == '__main__':
    Config.print_config()
