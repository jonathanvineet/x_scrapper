# 🚀 Generic Twitter Scraper

**A fully configurable Twitter/X scraper that works for ANY topic - sports, tech, news, entertainment, or anything else!**

## ✨ Features

- 🎯 **100% Generic** - No hardcoded content, search ANY topic
- 👥 **Account-Based Scraping** - Most reliable method
- 🔍 **Keyword Filtering** - Filter scraped tweets by keywords
- 💾 **SQLite Database** - All data saved in easy-to-query format
- 🚫 **No Login Required** - Uses Nitter (Twitter frontend)
- 🆓 **Completely Free** - No API costs
- ⚙️ **Multiple Input Methods** - CLI args, config files, or interactive mode

---

## ⚡ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run It!
```bash
# Generic scraper - works for ANY topic
python generic_scraper.py -a "CNN,BBC,Reuters" -m 20

# Or use interactive mode
python generic_scraper.py
```

**That's it!** 🎉

---

## 📚 Usage Examples

### News & Current Events
```bash
python generic_scraper.py -a "CNN,BBCWorld,Reuters,AP" -m 20
```

### Sports
```bash
python generic_scraper.py -a "ESPN,NBA,NFL" -m 20
```

### Technology
```bash
python generic_scraper.py -a "TechCrunch,TheVerge,WIRED" -m 20
```

### Entertainment
```bash
python generic_scraper.py -a "Variety,THR,Netflix" -m 20
```

### Business & Finance
```bash
python generic_scraper.py -a "business,Forbes,WSJ,Bloomberg" -m 20
```

### Science & Space
```bash
python generic_scraper.py -a "NASA,SpaceX,NatGeo" -m 20
```

### ANY Topic - Just Change the Accounts!
```bash
python generic_scraper.py -a "your,accounts,here" -m 20
```

---

## 🎓 How It Works

The scraper works by **scraping specific Twitter accounts** (not searching for keywords).

### Formula:
1. **Think of accounts** that tweet about your topic
2. **Run the scraper** with those accounts
3. **Get tweets** saved to SQLite database

### Example: For "Climate Change"
```bash
# Find relevant accounts: NASA_Climate, NOAA, GretaThunberg
python generic_scraper.py -a "NASA_Climate,NOAA,GretaThunberg" -m 20
```

### Why Accounts, Not Keywords?
- ✅ **Account scraping** = Reliable, proven to work
- ❌ **Keyword search** = Unreliable (Nitter limitations)

---

## 💻 Installation

```bash
# Clone the repository
git clone https://github.com/jonathanvineet/x_scrapper.git
cd x_scrapper

# Install dependencies
pip install -r requirements.txt

# Run it!
python generic_scraper.py
```

### Requirements
- Python 3.8+
- Chrome/Chromium browser
- Internet connection

---

## 🎯 Crypto-Specific Scraper

We also include a pre-configured crypto scraper:

```bash
python scrape_crypto_fast.py
```

This scrapes crypto-related tweets from major influencers like:
- VitalikButerin, cz_binance, APompliano
- Saylor, aantonop, balajis
- And more crypto accounts!

---

## ⚙️ Configuration

### Command-Line Options
```bash
python generic_scraper.py [OPTIONS]

Options:
  -a, --accounts       Twitter accounts to scrape (comma-separated)
  -k, --keywords       Keywords to filter tweets (optional)
  -m, --max-tweets     Maximum tweets per account (default: 20)
  -d, --database       Database filename (default: scraped_tweets.db)
  --no-display         Don't display results (only save)
  -h, --help           Show help message
```

### Interactive Mode
Just run without arguments:
```bash
python generic_scraper.py
```

### Environment Variables (Optional)
Store API credentials in `.env`:
```bash
X_CONSUMER_KEY=your_key_here
X_SECRET_KEY=your_secret_here
X_BEARER_TOKEN=your_token_here
```

---

## 📊 Viewing Results

### SQLite Command Line
```bash
# View tweets
sqlite3 scraped_tweets.db "SELECT username, text FROM tweets LIMIT 10;"

# Count tweets
sqlite3 scraped_tweets.db "SELECT COUNT(*) FROM tweets;"

# Export to CSV
sqlite3 -header -csv scraped_tweets.db "SELECT * FROM tweets;" > results.csv
```

### Database Schema
| Column | Description |
|--------|-------------|
| username | Twitter handle |
| text | Tweet content |
| timestamp | When posted |
| likes | Like count |
| retweets | Retweet count |
| replies | Reply count |
| keyword | Search keyword (if any) |
| scraped_at | When scraped |

---

## 🔧 Troubleshooting

### No Tweets Found?
- ✅ **Use accounts** instead of keywords only
- ✅ Try different accounts
- ✅ Wait a few minutes (rate limits)
- ✅ Check internet connection

### Rate Limited?
- The scraper automatically tries multiple Nitter instances
- Wait 5-10 minutes and try again
- Reduce max tweets (`-m 10`)

---

## 📖 Finding Accounts for Your Topic

For **any topic**, think of:
1. **News outlets** that cover it
2. **Companies** involved
3. **Organizations** in that field
4. **Experts/Influencers**
5. **Official accounts**

### Examples:
- **Politics**: `WhiteHouse`, `POTUS`, `SenateGOP`
- **Gaming**: `PlayStation`, `Xbox`, `NintendoAmerica`
- **Fashion**: `Vogue`, `GQ`, `ELLEmagazine`
- **Food**: `Tasty`, `foodnetwork`, `BonAppetit`

**Tip**: Google "twitter accounts [your topic]"

---

## 🎯 Advanced Usage

### Filter by Keywords
```bash
# Get only AI-related tweets from tech CEOs
python generic_scraper.py -a "elonmusk,BillGates,sundarpichai" -k "AI,artificial intelligence"
```

### Silent Mode (Large Datasets)
```bash
python generic_scraper.py -a "account1,account2" -m 50 --no-display
```

### Custom Database
```bash
python generic_scraper.py -a "ESPN,NBA" -d sports_analysis.db
```

---

## 🏗️ Project Structure

```
x_scrapper/
├── generic_scraper.py          # Main generic scraper (USE THIS!)
├── scrape_crypto_fast.py       # Pre-configured crypto scraper
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (optional)
├── .gitignore                 # Git ignore rules
└── README.md                   # This file
```

---

## 🎉 Success Stories

✅ **Sports**: Successfully scraped 20 tweets from ESPN & NFL  
✅ **Generic**: Works for ANY topic - just specify accounts  
✅ **Fast**: Scrapes 15-20 tweets in under 30 seconds  
✅ **Reliable**: Account-based scraping proven to work  

---

## 📝 License

MIT License - feel free to use for educational and research purposes.

---

## ⚠️ Disclaimer

This tool is for educational and research purposes only. Web scraping may violate Twitter's Terms of Service. Use responsibly and respect rate limits. For production use, consider using Twitter's official API.

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

**Made with ❤️ for the open-source community**

🌟 **Star this repo** if you find it useful!
