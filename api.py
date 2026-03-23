#!/usr/bin/env python3
"""
Flask API server for crypto scraper with scheduled background tasks
"""

from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import json
import logging
import threading
import time
from datetime import datetime
from scrape_crypto_fast import setup_driver, scrape_account
import os

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Database configuration
DATABASE_PATH = os.getenv('DATABASE_PATH', 'crypto_intelligence.db')

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database if it doesn't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scraped_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account TEXT,
            tweet_text TEXT,
            tweet_time TEXT,
            likes INTEGER,
            retweets INTEGER,
            replies INTEGER,
            sentiment REAL,
            importance_score REAL,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scrape_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT,
            message TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def run_scraper():
    """Run the scraper function"""
    try:
        logger.info("🚀 Starting crypto scraper...")
        driver = setup_driver()
        
        # List of accounts to scrape
        nitter_url = "https://nitter.1d4.us"
        accounts = [
            "elonmusk", "vitalikbuterin", "SBF_FTX", "cz_binance",
            "aantonop", "BTC", "crypto", "ethereum"
        ]
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        for account in accounts:
            try:
                result = scrape_account(driver, nitter_url, account)
                if result:
                    for tweet_data in result:
                        cursor.execute('''
                            INSERT INTO scraped_data 
                            (account, tweet_text, tweet_time, likes, retweets, replies, sentiment, importance_score)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            account,
                            tweet_data.get('text'),
                            tweet_data.get('time'),
                            tweet_data.get('likes', 0),
                            tweet_data.get('retweets', 0),
                            tweet_data.get('replies', 0),
                            tweet_data.get('sentiment', 0.0),
                            tweet_data.get('importance', 0.0)
                        ))
            except Exception as e:
                logger.error(f"Error scraping {account}: {e}")
        
        conn.commit()
        
        # Log successful scrape
        cursor.execute('INSERT INTO scrape_logs (status, message) VALUES (?, ?)',
                      ('success', f'Successfully scraped {len(accounts)} accounts'))
        conn.commit()
        conn.close()
        
        driver.quit()
        logger.info("✅ Scraper completed successfully")
        
    except Exception as e:
        logger.error(f"❌ Scraper error: {e}")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO scrape_logs (status, message) VALUES (?, ?)',
                      ('error', str(e)))
        conn.commit()
        conn.close()

def scheduler():
    """Run scraper every hour"""
    while True:
        try:
            run_scraper()
            logger.info("⏰ Next scrape in 1 hour...")
            time.sleep(3600)  # Run every hour
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
            time.sleep(60)

# Start scheduler in background thread
scheduler_thread = threading.Thread(target=scheduler, daemon=True)
scheduler_thread.start()

# Initialize database on startup
init_db()

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()}), 200

@app.route('/api/scrape', methods=['POST'])
def trigger_scrape():
    """Manually trigger scraper"""
    try:
        thread = threading.Thread(target=run_scraper, daemon=True)
        thread.start()
        return jsonify({'status': 'scraping', 'message': 'Scraper started'}), 202
    except Exception as e:
        logger.error(f"Error triggering scrape: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/results', methods=['GET'])
def get_results():
    """Get latest scraped results"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get latest 100 results
        cursor.execute('''
            SELECT account, tweet_text, tweet_time, likes, retweets, replies, 
                   sentiment, importance_score, scraped_at
            FROM scraped_data
            ORDER BY scraped_at DESC
            LIMIT 100
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        results = [dict(row) for row in rows]
        
        return jsonify({
            'status': 'success',
            'count': len(results),
            'data': results,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching results: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/results/<account>', methods=['GET'])
def get_account_results(account):
    """Get results for specific account"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT account, tweet_text, tweet_time, likes, retweets, replies, 
                   sentiment, importance_score, scraped_at
            FROM scraped_data
            WHERE account = ?
            ORDER BY scraped_at DESC
            LIMIT 50
        ''', (account,))
        
        rows = cursor.fetchall()
        conn.close()
        
        results = [dict(row) for row in rows]
        
        return jsonify({
            'status': 'success',
            'account': account,
            'count': len(results),
            'data': results,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching results: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    """Get scraper logs"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT status, message, scraped_at
            FROM scrape_logs
            ORDER BY scraped_at DESC
            LIMIT 50
        ''')
        
        rows = cursor.fetchall()
        conn.close()
        
        logs = [dict(row) for row in rows]
        
        return jsonify({
            'status': 'success',
            'logs': logs,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching logs: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) as total FROM scraped_data')
        total = cursor.fetchone()['total']
        
        cursor.execute('SELECT COUNT(DISTINCT account) as accounts FROM scraped_data')
        accounts = cursor.fetchone()['accounts']
        
        cursor.execute('SELECT AVG(likes) as avg_likes, MAX(likes) as max_likes FROM scraped_data')
        likes_stats = cursor.fetchone()
        
        conn.close()
        
        return jsonify({
            'status': 'success',
            'total_tweets': total,
            'unique_accounts': accounts,
            'avg_likes': likes_stats['avg_likes'] or 0,
            'max_likes': likes_stats['max_likes'] or 0,
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=False)
