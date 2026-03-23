# 🚀 Crypto Scraper API - Complete Implementation Guide

**Production-ready cryptocurrency market intelligence scraper with REST API, automatic hourly execution, and Vercel deployment.**

<div align="center">

![Status](https://img.shields.io/badge/Status-Production-brightgreen)
![API](https://img.shields.io/badge/API-6%20Endpoints-blue)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Deployment](https://img.shields.io/badge/Deployment-Vercel-black)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)

**[🌐 Live API](https://x-scrapper-wheat.vercel.app)**

</div>

---

## ✨ Features

- 🎯 **Smart Crypto Scraping** - Monitors 8+ major influencers & accounts
- 🌐 **REST API** - 6 endpoints for easy integration
- ⏱️ **Auto-Scheduled** - Runs automatically every hour
- 💾 **SQLite Database** - All data saved & queryable
- ☁️ **Vercel Deployed** - Production-ready serverless
- 🔒 **Error Handling** - Robust & reliable
- 📊 **Analytics Ready** - Sentiment & importance scores

---

## ⚡ Quick Start (5 Minutes)

### 1. Clone & Setup
```bash
git clone https://github.com/jonathanvineet/x_scrapper.git
cd x_scrapper
./setup.sh
```

### 2. Access API Locally
```bash
curl http://localhost:3000/api/health
```

### 3. Deploy to Vercel
```bash
./deploy.sh
```

**Done!** Your API is live 🎉

---

## � How to Implement Everything

### Step 1: Local Development (10 minutes)
```bash
# Setup everything
./setup.sh

# This does:
# - Creates virtual environment
# - Installs dependencies
# - Initializes database
# - Starts API server on http://localhost:3000
```

### Step 2: Test Endpoints (2 minutes)
```bash
# In another terminal
curl http://localhost:3000/api/health
curl http://localhost:3000/api/results
curl -X POST http://localhost:3000/api/scrape
```

### Step 3: Deploy to Vercel (5 minutes)
```bash
# One command deployment
./deploy.sh

# Or manually:
# 1. npm i -g vercel
# 2. vercel login
# 3. vercel --prod
```

### Step 4: Enable Hourly Scraping (2 minutes)
Visit https://cron-job.org:
- Create cron job
- URL: Your Vercel domain + `/api/scrape`
- Schedule: Every 1 hour
- Save

**Total time: ~20 minutes from zero to production!**

---

## 📊 Complete Scraping Setup

### What Gets Scraped

**Default Monitored Accounts:**
- elonmusk - Elon Musk
- vitalikbuterin - Vitalik Buterin (Ethereum founder)
- SBF_FTX - Sam Bankman-Fried (FTX founder)
- cz_binance - Changpeng Zhao (Binance CEO)
- aantonop - Andreas M. Antonopoulos (Bitcoin expert)
- BTC - Bitcoin account
- crypto - Crypto general account
- ethereum - Ethereum account

**Per Tweet Collected:**
- Tweet text/content
- Engagement: likes, retweets, replies
- Timestamp posted
- Sentiment score (-1.0 to 1.0)
- Importance score (0.0 to 1.0)
- Account that posted it

### How Scraping Works

```
1. Scheduler triggers every hour
   ↓
2. Connect to Nitter (Twitter frontend)
   ↓
3. Fetch tweets from each account
   ↓
4. Parse tweet data (text, engagement, time)
   ↓
5. Calculate sentiment & importance
   ↓
6. Save to SQLite database
   ↓
7. Log success/failure
```

### Customizing Accounts

Edit `api/index.py`, around line 60:
```python
accounts = [
    "your_account_1",
    "your_account_2",
    "your_account_3",
    # Add any Twitter accounts you want to monitor
]
```

Then redeploy:
```bash
vercel --prod --yes
```

### Market-Moving Keywords Detected

The scraper automatically identifies important tweets with keywords like:

**Crypto Keywords:**
bitcoin, btc, ethereum, eth, defi, blockchain, nft, token, altcoin, hodl

**Regulatory:**
regulation, SEC, CFTC, compliance, enforcement, ban, lawsuit

**Market:**
bull, bear, pump, dump, moon, crash, ATH, support, resistance

**Geopolitics:**
war, sanctions, embargo, conflict, cyberattack

---

## 🔌 All 6 API Endpoints Explained

### 1. GET /api/health
**Purpose:** Check if API is online and database is connected

**Response:**
```json
{
  "status": "ok",
  "database": "connected",
  "timestamp": "2026-03-23T10:30:00"
}
```

### 2. GET /api/results
**Purpose:** Get latest 100 scraped tweets

**Response:**
```json
{
  "status": "success",
  "count": 100,
  "data": [
    {
      "account": "elonmusk",
      "tweet_text": "Bitcoin is freedom...",
      "tweet_time": "2026-03-23 10:25:00",
      "likes": 45000,
      "retweets": 12000,
      "replies": 3000,
      "sentiment": 0.85,
      "importance_score": 0.95,
      "scraped_at": "2026-03-23T10:30:00"
    }
  ],
  "timestamp": "2026-03-23T10:30:00"
}
```

### 3. GET /api/results/:account
**Purpose:** Get tweets from specific account

**Example:** `GET /api/results/elonmusk`

**Response:** Same as #2 but filtered by account

### 4. POST /api/scrape
**Purpose:** Manually trigger scraper (runs in background)

**Response:**
```json
{
  "status": "scraping",
  "message": "Scraper started"
}
```

### 5. GET /api/logs
**Purpose:** View execution history

**Response:**
```json
{
  "status": "success",
  "logs": [
    {
      "status": "success",
      "message": "Successfully scraped 500 tweets from 8 accounts",
      "scraped_at": "2026-03-23T10:00:00"
    }
  ]
}
```

### 6. GET /api/stats
**Purpose:** Get database statistics

**Response:**
```json
{
  "status": "success",
  "total_tweets": 2500,
  "unique_accounts": 8,
  "avg_likes": 15000,
  "max_likes": 150000,
  "timestamp": "2026-03-23T10:30:00"
}
```

---

## ⚙️ Configuration Guide

### Environment Variables (.env.local)
```bash
# Database
DATABASE_PATH=/tmp/crypto_intelligence.db

# Scraper options
USE_SELENIUM=true
HEADLESS=true
MONITORING_INTERVAL=300

# Thresholds
HIGH_ENGAGEMENT_THRESHOLD=10000
SENTIMENT_THRESHOLD=0.5

# X/Twitter API (optional)
X_BEARER_TOKEN=your_token
TWITTER_BEARER_TOKEN=your_token
```

### Application Config (config.py)
```python
class Config:
    # Database
    DATABASE_PATH = os.getenv('DATABASE_PATH', 'crypto_intelligence.db')
    
    # Scraping
    USE_SELENIUM = os.getenv('USE_SELENIUM', 'true').lower() == 'true'
    HEADLESS = os.getenv('HEADLESS', 'true').lower() == 'true'
    MAX_TWEETS_PER_ACCOUNT = int(os.getenv('MAX_TWEETS_PER_ACCOUNT', '50'))
    
    # Limits
    HIGH_ENGAGEMENT_THRESHOLD = int(os.getenv('HIGH_ENGAGEMENT_THRESHOLD', '10000'))
```

---

## 🚀 Complete Deployment Steps

### Local Setup
```bash
# 1. Clone
git clone https://github.com/jonathanvineet/x_scrapper.git
cd x_scrapper

# 2. Setup (automated)
./setup.sh

# 3. Test
curl http://localhost:3000/api/health

# 4. (Optional) View database
sqlite3 /tmp/crypto_intelligence.db "SELECT COUNT(*) FROM scraped_data;"
```

### Vercel Deployment
```bash
# 1. Install Vercel CLI
npm i -g vercel

# 2. Login
vercel login

# 3. Deploy
vercel --prod --yes

# 4. Your API is live at:
# https://x-scrapper-wheat.vercel.app
```

### Enable Automatic Hourly Execution

**Option A: cron-job.org** (RECOMMENDED)
```
1. Go to https://cron-job.org
2. Create new cron job
3. Set URL to your API + /api/scrape
4. Schedule: Every 1 hour
5. Save
```

**Option B: GitHub Actions** (BUILT-IN)
```
1. Go to your GitHub repo
2. Settings → Secrets
3. Add SCRAPER_API_URL = your-domain.vercel.app
4. Workflows automatically trigger hourly
```

**Option C: Local Cron** (Linux/macOS)
```bash
# Edit crontab
crontab -e

# Add line:
0 * * * * curl -X POST https://YOUR_DOMAIN/api/scrape
```

---

## 📚 Using the API

### In JavaScript
```javascript
const response = await fetch('https://x-scrapper-wheat.vercel.app/api/results');
const data = await response.json();

// Get most important tweets
const important = data.data.filter(t => t.importance_score > 0.8);
console.log(important);
```

### In Python
```python
import requests
import json

response = requests.get('https://x-scrapper-wheat.vercel.app/api/results')
data = response.json()

# Filter by sentiment
positive = [t for t in data['data'] if t['sentiment'] > 0.5]
print(json.dumps(positive, indent=2))
```

### In Bash/cURL
```bash
# Get latest tweets
curl https://x-scrapper-wheat.vercel.app/api/results | jq '.data[0]'

# Get high-engagement tweets
curl https://x-scrapper-wheat.vercel.app/api/results | jq '.data[] | select(.likes > 50000)'

# Get stats
curl https://x-scrapper-wheat.vercel.app/api/stats | jq '.'
```

---

## 🗄️ Database Guide

### View Database Locally
```bash
# Install sqlite3 if needed
# macOS: brew install sqlite3
# Linux: apt-get install sqlite3
# Windows: download from sqlite.org

# Connect to database
sqlite3 /tmp/crypto_intelligence.db

# View tables
.tables

# View schema
.schema scraped_data
.schema scrape_logs

# Query data
SELECT * FROM scraped_data LIMIT 5;
SELECT COUNT(*) FROM scraped_data;
SELECT account, COUNT(*) FROM scraped_data GROUP BY account;

# Export to CSV
.mode csv
.output results.csv
SELECT * FROM scraped_data;
.output stdout
```

### Database Schema

**scraped_data table:**
```
id              - Unique ID
account         - Twitter account name
tweet_text      - Tweet content
tweet_time      - When posted
likes           - Like count
retweets        - Retweet count
replies         - Reply count
sentiment       - Sentiment score (-1 to 1)
importance_score - Importance score (0 to 1)
scraped_at      - When scraped
```

**scrape_logs table:**
```
id          - Unique ID
status      - success/error
message     - Log message
scraped_at  - When logged
```

---

## 🐛 Troubleshooting

### API Returns 500 Error
```bash
# Check Vercel logs
vercel logs --follow

# Test locally
python api/index.py

# Check database connection
python3 << 'EOF'
import sqlite3
conn = sqlite3.connect('/tmp/crypto_intelligence.db')
print("✅ Connected")
conn.close()
EOF
```

### Scraper Not Running
```bash
# Check cron-job.org is enabled and active
# View execution logs
curl https://YOUR_DOMAIN/api/logs | jq '.logs[0]'

# Manually trigger
curl -X POST https://YOUR_DOMAIN/api/scrape

# Check Vercel logs
vercel logs --follow
```

### No Data in Database
```bash
# Database might be empty initially
# Manually trigger scraper
curl -X POST https://YOUR_DOMAIN/api/scrape

# Wait a minute, then check
curl https://YOUR_DOMAIN/api/stats
```

### Deployment Failed
```bash
# Clear cache and redeploy
rm -rf .vercel
vercel --prod --yes
```

---

## 📈 Monitoring Your Scraper

### Real-Time Health Check
```bash
# Check every 10 seconds
watch -n 10 'curl https://YOUR_DOMAIN/api/health | jq'
```

### Monitor Execution Logs
```bash
# View live logs
vercel logs --follow

# View API logs
curl https://YOUR_DOMAIN/api/logs | jq '.logs[0:10]'
```

### Track Statistics
```bash
# Check growth
watch -n 60 'curl https://YOUR_DOMAIN/api/stats | jq'
```

---

## 🔍 Getting Data from Vercel

### View Deployment Information
```bash
# List all deployments
vercel list

# View specific deployment details
vercel inspect [DEPLOYMENT_URL]

# Get current project info
vercel projects list
```

### Access Your Live API Domain
```bash
# Get your Vercel domain
vercel list

# Output shows:
# URL: https://x-scrapper-wheat.vercel.app
# Created: ...
```

### View Real-Time Logs
```bash
# Stream live logs (best for debugging)
vercel logs --follow

# View last 100 lines
vercel logs

# View logs for specific deployment
vercel logs [DEPLOYMENT_URL]

# Filter by log level
vercel logs --follow --level error
```

### Check Environment Variables
```bash
# List all environment variables
vercel env list

# View specific env var
vercel env list DATABASE_PATH
```

### View Function Metrics
```bash
# Check function execution time & memory
vercel projects inspect

# View in dashboard: https://vercel.com/dashboard
```

### Access Vercel Dashboard

**Open in browser:**
```
https://vercel.com/dashboard
```

**Then navigate to:**
1. Select `x-scrapper` project
2. **Deployments tab** - View all deployments
3. **Logs tab** - Real-time function logs
4. **Settings tab** - Configuration & environment variables
5. **Integrations** - GitHub, analytics, etc.

### Get Your API Domain & Details
```bash
# Method 1: Via CLI
vercel list

# Method 2: Via Dashboard
# 1. Go to https://vercel.com/dashboard
# 2. Click x-scrapper project
# 3. Domain shown at top: x-scrapper-wheat.vercel.app

# Method 3: Check deployment URL
vercel projects inspect x-scrapper
```

### Monitor Function Execution

**Via Vercel Dashboard:**
1. Go to https://vercel.com/dashboard
2. Select x-scrapper project
3. Click on a deployment
4. View:
   - Response status
   - Execution time
   - Memory used
   - Errors/logs

**Via CLI:**
```bash
# View function details
vercel inspect https://x-scrapper-wheat.vercel.app

# Get detailed metrics
vercel projects inspect --json
```

### Export & Backup Data

**From Your API:**
```bash
# Export all results to JSON
curl https://x-scrapper-wheat.vercel.app/api/results > results.json

# Export stats
curl https://x-scrapper-wheat.vercel.app/api/stats > stats.json

# Export logs
curl https://x-scrapper-wheat.vercel.app/api/logs > logs.json
```

**From SQLite Database:**
```bash
# Export to CSV
sqlite3 /tmp/crypto_intelligence.db ".mode csv" ".output results.csv" "SELECT * FROM scraped_data;" ".output stdout"

# Export to JSON
sqlite3 /tmp/crypto_intelligence.db ".mode json" "SELECT * FROM scraped_data;" > results.json
```

### Get Deployment Logs Programmatically

```bash
# Get last 50 lines of logs in JSON
vercel logs --json > deployment_logs.json

# Get error logs only
vercel logs --level error --json > errors.json

# Get logs from specific time
vercel logs --since 1h --json
```

### Access Raw Function Output

**Function logs endpoint:**
```bash
# View deployment build logs
https://vercel.com/jonathans-projects-e5e7401f/x-scrapper/deployments

# Each deployment shows:
# - Build logs (stdout/stderr)
# - Execution logs
# - Error messages
# - Performance metrics
```

### Monitor API Performance

**Check response times:**
```bash
# Measure API response time
time curl https://x-scrapper-wheat.vercel.app/api/health

# Expected: < 200ms
```

**Track metrics in Vercel:**
1. Dashboard → x-scrapper project
2. Analytics tab (if enabled)
3. View:
   - Response time
   - Request count
   - Error rate

### Redeploy from Vercel Dashboard

**Method 1: Via CLI**
```bash
vercel --prod --yes
```

**Method 2: Via Dashboard**
1. https://vercel.com/dashboard
2. Select x-scrapper
3. Click on a deployment
4. Click "..." menu
5. Select "Redeploy"

**Method 3: Auto-deploy on Git Push**
```bash
# Just push to GitHub
git push origin main

# Vercel automatically deploys!
```

### Get Deployment URL

```bash
# After deployment
vercel --prod

# Output shows:
# Production: https://x-scrapper-wheat.vercel.app
# Inspect: https://vercel.com/...

# Your API is at the Production URL
```

### Share Your API

```bash
# Copy your domain
https://x-scrapper-wheat.vercel.app

# Share to others:
# - Give them the /api/results endpoint
# - They can query your live data!

# Example for others:
curl https://x-scrapper-wheat.vercel.app/api/stats
```

### Troubleshoot via Logs

**Find errors:**
```bash
# Search logs for errors
vercel logs --follow | grep -i error

# Get function execution details
vercel logs --follow --level error

# Check database connection errors
vercel logs | grep -i "database\|connection"
```

**Common log messages:**
```
✅ "Database initialized" - Good!
✅ "Scraper completed successfully" - Good!
❌ "Database connection error" - Check DATABASE_PATH
❌ "Module not found" - Check requirements.txt
❌ "Timeout" - Function taking too long
```

### Access Deployment Files

**View deployed code:**
```bash
# List project files
vercel ls

# View file contents
vercel cat path/to/file
```

**View on dashboard:**
1. https://vercel.com/dashboard
2. x-scrapper project
3. Deployments tab
4. Click deployment
5. Files tab (shows what was deployed)

---

## ✅ Complete Checklist

- [ ] Read this README
- [ ] Run ./setup.sh locally
- [ ] Test all 6 endpoints
- [ ] Deploy with ./deploy.sh
- [ ] Set up hourly scraping (cron-job.org)
- [ ] Monitor with vercel logs --follow
- [ ] Check API stats daily
- [ ] Add custom accounts if needed
- [ ] Set up alerts (optional)
- [ ] Add authentication (optional)

---

## 📚 More Documentation

| Document | Purpose |
|----------|---------|
| **API_DOCS.md** | Complete API reference |
| **DEPLOYMENT.md** | Advanced deployment options |
| **DEPLOYMENT_SUCCESS.md** | Deployment status details |
| **DEPLOYMENT_REPORT.md** | Technical implementation details |
| **QUICKSTART.md** | 5-minute quick start |

---

## 🔒 Production Best Practices

1. **Keep .env Secure**
   - Never commit to Git
   - Store secrets in Vercel Settings

2. **Monitor Logs**
   - Check daily: `vercel logs --follow`
   - Set up alerts

3. **Database Maintenance**
   - For production: Use PostgreSQL instead of SQLite
   - SQLite on Vercel is ephemeral (resets on redeploy)

4. **Add Authentication**
   - Protect endpoints with API keys
   - See DEPLOYMENT.md for example

5. **Rate Limiting**
   - Use Flask-Limiter to prevent abuse
   - Set reasonable limits

6. **Backups**
   - Export data regularly
   - Store important results

---

## 🎉 You're All Set!

Your crypto scraper is fully implemented and ready to use!

**API Domain:** https://x-scrapper-wheat.vercel.app

**Next Steps:**
1. ✅ API deployed
2. ⏳ Set up hourly scraping (cron-job.org)
3. 📊 Monitor execution logs
4. 🔧 Customize accounts if needed
5. 🚀 Integrate into your application

---

## 📞 Support & Resources

- **Issues?** Check DEPLOYMENT_REPORT.md → Troubleshooting
- **API Help?** See API_DOCS.md
- **Deploy Help?** See DEPLOYMENT.md
- **Quick Start?** See QUICKSTART.md

---

<div align="center">

**Made with ❤️ for crypto market intelligence**

[🌐 Live API](https://x-scrapper-wheat.vercel.app) | [⭐ Star on GitHub](https://github.com/jonathanvineet/x_scrapper) | [📖 Docs](API_DOCS.md)

</div>
