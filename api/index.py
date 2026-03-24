import os
import time
import json
import logging
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
import requests
import xml.etree.ElementTree as ET
import concurrent.futures

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Lightweight in-memory cache to prevent repeated fetching in reused lambda contexts
CACHE = {
    "data": [],
    "last_fetch": 0,
    "stats": {
        "total_tweets": 0,
        "unique_accounts": 0,
        "avg_likes": 0,
        "max_likes": 0
    }
}
CACHE_TTL = 30  # 30 seconds cache

# Extremely reliable unblocked feeds representing market news/signals
TARGET_FEEDS = [
    {"account": "CoinTelegraph", "url": "https://cointelegraph.com/rss"},
    {"account": "CoinDesk", "url": "https://www.coindesk.com/arc/outboundfeeds/rss/"},
    {"account": "CryptoNews", "url": "https://cryptonews.com/news/feed/"},
    {"account": "NewsBTC", "url": "https://www.newsbtc.com/feed/"},
    {"account": "BitcoinMagazine", "url": "https://bitcoinmagazine.com/.rss/full/"}
]

MARKET_KEYWORDS = [
    'btc', 'bitcoin', 'eth', 'ethereum', 'crypto', 'defi', 'solana', 'bull', 'bear',
    'pump', 'dump', 'sec', 'cftc', 'lawsuit', 'banned', 'regulation', 'fomc', 'interest rates',
    'breaking', 'urgent', 'hack', 'exploit', 'stolen', 'liquidation', 'blackrock', 'etf'
]

def fetch_crypto_rss(feed_meta):
    account = feed_meta["account"]
    url = feed_meta["url"]
    results = []
    
    try:
        response = requests.get(url, timeout=5, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/rss+xml, application/rdf+xml, application/atom+xml, application/xml, text/xml"
        })
        
        if response.status_code != 200:
            logger.error(f"Failed to fetch {account}: {response.status_code}")
            return account, results
            
        root = ET.fromstring(response.content)
        
        # Depending on whether it's RSS (channel->item) or Atom feed
        items = root.findall(".//item")
        if not items:
            items = root.findall("{http://www.w3.org/2005/Atom}entry")
            
        for item in items[:20]: # Parse top 20 news items
            title_el = item.find("title")
            if title_el is None:
                title_el = item.find("{http://www.w3.org/2005/Atom}title")
                
            pub_date_el = item.find("pubDate")
            if pub_date_el is None:
                pub_date_el = item.find("{http://www.w3.org/2005/Atom}published")
                if pub_date_el is None:
                    pub_date_el = item.find("{http://www.w3.org/2005/Atom}updated")
            
            title = title_el.text if title_el is not None else ""
            pub_date = pub_date_el.text if pub_date_el is not None else datetime.now().isoformat()
            
            text_lower = title.lower()
            importance = 1.0 if any(kw in text_lower for kw in MARKET_KEYWORDS) else 0.4
            
            # Map standard RSS news metrics into Cerberus expected Tweet schema
            results.append({
                "account": account,
                "tweet_text": title,
                "tweet_time": pub_date,
                "likes": int(importance * 5000), # Simulated engagement for UI layout
                "retweets": int(importance * 1000), 
                "replies": int(importance * 200),
                "sentiment": 0.0,
                "importance_score": importance,
                "scraped_at": datetime.now().isoformat()
            })
    except Exception as e:
        logger.error(f"Error parsing RSS API for {account}: {e}")
        
    return account, results

def get_live_signals():
    global CACHE
    now = time.time()
    
    # Return cache if valid (prevents Vercel rate limits and timeouts)
    if CACHE["data"] and (now - CACHE["last_fetch"] < CACHE_TTL):
        return CACHE["data"]
        
    all_signals = []
    
    # Fetch in parallel for speed (< 2-3 seconds total for all accounts)
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(TARGET_FEEDS)) as executor:
        futures = {executor.submit(fetch_crypto_rss, feed): feed["account"] for feed in TARGET_FEEDS}
        for future in concurrent.futures.as_completed(futures):
            account, account_signals = future.result()
            all_signals.extend(account_signals)
    
    # Sort by importance, then by recency
    all_signals.sort(key=lambda x: x["importance_score"], reverse=True)
    
    CACHE["data"] = all_signals
    CACHE["last_fetch"] = now
    
    total_likes = sum(t.get("likes", 0) for t in all_signals)
    
    CACHE["stats"] = {
        "total_tweets": len(all_signals),
        "unique_accounts": len(set(t["account"] for t in all_signals)),
        "avg_likes": int(total_likes / len(all_signals)) if all_signals else 0,
        "max_likes": max([t.get("likes", 0) for t in all_signals]) if all_signals else 0
    }
    
    return all_signals

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'status': 'ok',
        'message': 'Cerberus Live Proxy API (Vercel Serverless Edition)',
        'endpoints': ['GET /api/health', 'GET /api/results', 'GET /api/stats']
    }), 200

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'database': 'proxy-mode (Reliable RSS V3)', 'timestamp': datetime.now().isoformat()}), 200

@app.route('/api/scrape', methods=['POST', 'GET'])
def trigger_scrape():
    # Force a cache refresh manually
    global CACHE
    CACHE["last_fetch"] = 0
    get_live_signals()
    return jsonify({'status': 'success', 'message': 'Cache refreshed synchronously'}), 200

@app.route('/api/results', methods=['GET'])
def get_results():
    try:
        results = get_live_signals()
        return jsonify({
            'status': 'success',
            'count': len(results),
            'data': results,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error fetching live results: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/results/<account>', methods=['GET'])
def get_account_results(account):
    try:
        results = get_live_signals()
        filtered = [t for t in results if t["account"].lower() == account.lower()]
        return jsonify({
            'status': 'success',
            'account': account,
            'count': len(filtered),
            'data': filtered,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error fetching results: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/logs', methods=['GET'])
def get_logs():
    return jsonify({
        'status': 'success',
        'logs': [{'status': 'success', 'message': 'Operating in synchronous Vercel proxy mode (RSS parsing). No background jobs ran.', 'scraped_at': datetime.now().isoformat()}],
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/stats', methods=['GET'])
def get_stats():
    get_live_signals()
    stats = CACHE["stats"]
    stats["status"] = "success"
    stats["timestamp"] = datetime.now().isoformat()
    return jsonify(stats), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 3000)), debug=False)
