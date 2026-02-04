#!/usr/bin/env python3
"""
Quick Start Script - Get up and running in seconds!
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if all required packages are installed"""
    print("🔍 Checking dependencies...")
    
    missing = []
    packages = {
        'selenium': 'selenium',
        'tweepy': 'tweepy',
        'pandas': 'pandas',
        'textblob': 'textblob',
        'bs4': 'beautifulsoup4',
        'requests': 'requests'
    }
    
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All dependencies installed!")
    return True


def setup_nltk():
    """Download required NLTK data"""
    print("\n📚 Setting up NLTK data...")
    try:
        import nltk
        try:
            nltk.data.find('tokenizers/punkt')
            print("  ✅ NLTK data already downloaded")
        except LookupError:
            print("  📥 Downloading NLTK data...")
            nltk.download('punkt', quiet=True)
            nltk.download('vader_lexicon', quiet=True)
            print("  ✅ NLTK data downloaded")
    except Exception as e:
        print(f"  ⚠️  Error: {e}")


def check_config():
    """Check if config file exists"""
    print("\n⚙️  Checking configuration...")
    
    if Path('config.json').exists():
        print("  ✅ config.json found")
        return True
    else:
        print("  ⚠️  config.json not found")
        
        if Path('config_template.json').exists():
            print("\n  Would you like to create config.json from template? (y/n): ", end='')
            response = input().strip().lower()
            
            if response == 'y':
                import shutil
                shutil.copy('config_template.json', 'config.json')
                print("  ✅ config.json created from template")
                print("  📝 Edit config.json to add your API credentials (optional)")
                return True
        
        print("  ℹ️  Using default configuration (Selenium only)")
        return False


def run_demo():
    """Run a quick demo"""
    print("\n" + "="*60)
    print("🎯 QUICK DEMO - Scraping a Sample Account")
    print("="*60)
    
    from crypto_scraper_orchestrator import CryptoTwitterIntelligence
    
    config = {
        'use_api': False,
        'use_selenium': True,
        'headless': True,
        'database_path': 'demo.db'
    }
    
    print("\n🚀 Initializing scraper (this may take a moment)...")
    scraper = CryptoTwitterIntelligence(config)
    
    try:
        print("📱 Scraping @VitalikButerin (5 tweets)...")
        tweets = scraper.scrape_account('VitalikButerin', max_tweets=5)
        
        if tweets:
            print(f"\n✅ Retrieved {len(tweets)} tweets!\n")
            
            for i, tweet in enumerate(tweets[:3], 1):
                print(f"─" * 60)
                print(f"Tweet {i}:")
                print(f"  📅 {tweet.timestamp}")
                print(f"  💬 {tweet.text[:200]}{'...' if len(tweet.text) > 200 else ''}")
                print(f"  ❤️  {tweet.likes} likes | 🔄 {tweet.retweets} retweets")
                print(f"  😊 Sentiment: {tweet.sentiment_label} ({tweet.sentiment_score:.2f})")
            
            print(f"\n📊 All {len(tweets)} tweets saved to demo.db")
            print("✅ Demo complete!")
            
        else:
            print("⚠️  No tweets retrieved. Check your internet connection.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Chrome/Chromium is installed")
        print("2. Check your internet connection")
        print("3. Try again (Twitter may have rate limited)")
        
    finally:
        scraper.cleanup()


def show_menu():
    """Show main menu"""
    print("\n" + "="*60)
    print("🚀 CRYPTO TWITTER INTELLIGENCE - QUICK START")
    print("="*60)
    print("\nWhat would you like to do?")
    print("\n1. 🧪 Run Quick Demo (recommended first time)")
    print("2. 📖 View Documentation")
    print("3. 🎓 Run Interactive Examples")
    print("4. ⚙️  Setup Configuration")
    print("5. 🏃 Start Full System")
    print("0. ❌ Exit")
    
    choice = input("\nEnter your choice (0-5): ").strip()
    return choice


def main():
    """Main entry point"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║        CRYPTO TWITTER INTELLIGENCE SYSTEM                    ║
║        Advanced Scraper for Web3 & Market Intelligence       ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first:")
        print("   pip install -r requirements.txt")
        return
    
    # Setup NLTK
    setup_nltk()
    
    # Check config
    check_config()
    
    # Show menu
    while True:
        choice = show_menu()
        
        if choice == '1':
            run_demo()
            input("\n Press Enter to continue...")
            
        elif choice == '2':
            print("\n📖 Opening README.md...")
            if Path('README.md').exists():
                print("\nREADME.md contains full documentation.")
                print("View it in your text editor or GitHub.")
                input("Press Enter to continue...")
            else:
                print("❌ README.md not found")
                
        elif choice == '3':
            print("\n🎓 Launching interactive examples...")
            try:
                import example_usage
                print("\n✅ Examples loaded. Choose an option from the menu.")
            except Exception as e:
                print(f"❌ Error loading examples: {e}")
            input("Press Enter to continue...")
            
        elif choice == '4':
            check_config()
            print("\n📝 Edit config.json with your preferred text editor")
            print("   API credentials are optional but recommended")
            input("Press Enter to continue...")
            
        elif choice == '5':
            print("\n🚀 Starting full system...")
            print("This will launch the main monitoring system.")
            print("⚠️  This is a long-running process. Use Ctrl+C to stop.")
            
            confirm = input("\nContinue? (y/n): ").strip().lower()
            if confirm == 'y':
                try:
                    from example_usage import example_3_monitoring
                    example_3_monitoring()
                except KeyboardInterrupt:
                    print("\n\n✅ Monitoring stopped")
                except Exception as e:
                    print(f"\n❌ Error: {e}")
            
        elif choice == '0':
            print("\n👋 Goodbye!")
            break
            
        else:
            print("\n❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Check logs or README.md for troubleshooting")
