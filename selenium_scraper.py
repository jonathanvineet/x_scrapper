"""
Selenium-based Twitter/X scraper
Handles dynamic content loading and advanced scraping
"""

import time
import logging
from typing import List, Dict, Optional
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class SeleniumTwitterScraper:
    """Advanced Selenium scraper with anti-detection"""
    
    def __init__(self, headless: bool = True, proxy: Optional[str] = None):
        self.headless = headless
        self.proxy = proxy
        self.driver = None
        
    def _init_driver(self):
        """Initialize Chrome WebDriver with stealth settings"""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            from selenium.webdriver.chrome.service import Service
            from webdriver_manager.chrome import ChromeDriverManager
            
            options = Options()
            
            # Essential container/headless options
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-software-rasterizer')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-setuid-sandbox')
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--remote-debugging-port=9222')
            options.add_argument('--disable-blink-features=AutomationControlled')
            
            # Realistic user agent
            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Additional anti-detection
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})
            
            if self.proxy:
                options.add_argument(f'--proxy-server={self.proxy}')
            
            # Use webdriver-manager to handle chromedriver
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            except:
                # Fallback to system chromedriver
                self.driver = webdriver.Chrome(options=options)
            
            # Execute CDP commands for further stealth
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            })
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
            
            self.driver.implicitly_wait(10)
            logger.info("Selenium WebDriver initialized")
            
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def scrape_user_timeline(self, username: str, max_tweets: int = 50, scroll_pause: float = 2.0) -> List[Dict]:
        """Scrape tweets from user timeline"""
        if not self.driver:
            self._init_driver()
        
        url = f"https://twitter.com/{username}"
        logger.info(f"Scraping timeline: {url}")
        
        try:
            self.driver.get(url)
            time.sleep(3)
            
            tweets = []
            seen_ids = set()
            last_height = 0
            no_new_content_count = 0
            max_no_content = 5
            
            while len(tweets) < max_tweets and no_new_content_count < max_no_content:
                # Find tweet elements
                from selenium.webdriver.common.by import By
                tweet_elements = self.driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
                
                initial_count = len(tweets)
                
                for element in tweet_elements:
                    try:
                        tweet_data = self._extract_tweet_from_element(element, username)
                        
                        if tweet_data and tweet_data['id'] not in seen_ids:
                            seen_ids.add(tweet_data['id'])
                            tweets.append(tweet_data)
                            logger.debug(f"Extracted tweet {len(tweets)}/{max_tweets}")
                            
                            if len(tweets) >= max_tweets:
                                break
                    except Exception as e:
                        logger.debug(f"Error extracting tweet: {e}")
                        continue
                
                # Check if we got new tweets
                if len(tweets) == initial_count:
                    no_new_content_count += 1
                else:
                    no_new_content_count = 0
                
                # Scroll down
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scroll_pause)
                
                # Check scroll position
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    no_new_content_count += 1
                last_height = new_height
            
            logger.info(f"Successfully scraped {len(tweets)} tweets from @{username}")
            return tweets
            
        except Exception as e:
            logger.error(f"Error scraping timeline: {e}")
            return []
    
    def search_tweets(self, query: str, max_tweets: int = 100, search_type: str = 'latest') -> List[Dict]:
        """
        Search tweets by query
        
        Args:
            query: Search query
            max_tweets: Maximum tweets to retrieve
            search_type: 'latest', 'top', or 'people'
        """
        if not self.driver:
            self._init_driver()
        
        # URL encode query
        from urllib.parse import quote
        encoded_query = quote(query)
        
        # Construct search URL
        if search_type == 'latest':
            url = f"https://twitter.com/search?q={encoded_query}&src=typed_query&f=live"
        elif search_type == 'top':
            url = f"https://twitter.com/search?q={encoded_query}&src=typed_query"
        else:
            url = f"https://twitter.com/search?q={encoded_query}&src=typed_query&f=user"
        
        logger.info(f"Searching: {url}")
        
        try:
            self.driver.get(url)
            time.sleep(4)
            
            tweets = []
            seen_ids = set()
            scroll_attempts = 0
            max_scrolls = 20
            
            while len(tweets) < max_tweets and scroll_attempts < max_scrolls:
                from selenium.webdriver.common.by import By
                tweet_elements = self.driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
                
                for element in tweet_elements:
                    try:
                        tweet_data = self._extract_tweet_from_element(element)
                        
                        if tweet_data and tweet_data['id'] not in seen_ids:
                            seen_ids.add(tweet_data['id'])
                            tweets.append(tweet_data)
                            
                            if len(tweets) >= max_tweets:
                                break
                    except:
                        continue
                
                # Scroll
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                scroll_attempts += 1
            
            logger.info(f"Found {len(tweets)} tweets for query: {query}")
            return tweets
            
        except Exception as e:
            logger.error(f"Error searching tweets: {e}")
            return []
    
    def _extract_tweet_from_element(self, element, default_username: str = None) -> Optional[Dict]:
        """Extract all data from a tweet element"""
        try:
            from selenium.webdriver.common.by import By
            
            # Extract username
            username = default_username
            if not username:
                try:
                    user_link = element.find_element(By.CSS_SELECTOR, 'a[role="link"][href^="/"]')
                    href = user_link.get_attribute('href')
                    username = href.split('/')[-3] if '/' in href else None
                except:
                    username = "unknown"
            
            # Extract tweet text
            text = ""
            try:
                text_element = element.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                text = text_element.text
            except:
                pass
            
            # Extract timestamp
            timestamp = None
            try:
                time_element = element.find_element(By.CSS_SELECTOR, 'time')
                timestamp = time_element.get_attribute('datetime')
            except:
                timestamp = datetime.now().isoformat()
            
            # Extract metrics
            metrics = self._extract_metrics(element)
            
            # Extract links and media
            links = []
            try:
                link_elements = element.find_elements(By.CSS_SELECTOR, 'a[href^="http"]')
                links = [elem.get_attribute('href') for elem in link_elements if elem.get_attribute('href')]
            except:
                pass
            
            # Generate ID
            tweet_id = f"{username}_{hash(text + str(timestamp))}"
            
            # Extract hashtags and mentions from text
            hashtags = re.findall(r'#(\w+)', text)
            mentions = re.findall(r'@(\w+)', text)
            
            return {
                'id': tweet_id,
                'username': username,
                'text': text,
                'timestamp': timestamp,
                'metrics': metrics,
                'hashtags': hashtags,
                'mentions': mentions,
                'urls': links
            }
            
        except Exception as e:
            logger.debug(f"Error in _extract_tweet_from_element: {e}")
            return None
    
    def _extract_metrics(self, element) -> Dict:
        """Extract engagement metrics from tweet element"""
        from selenium.webdriver.common.by import By
        
        metrics = {
            'likes': 0,
            'retweets': 0,
            'replies': 0,
            'views': 0
        }
        
        try:
            # Likes
            try:
                like_button = element.find_element(By.CSS_SELECTOR, '[data-testid="like"]')
                like_text = like_button.get_attribute('aria-label') or like_button.text
                metrics['likes'] = self._parse_number(like_text)
            except:
                pass
            
            # Retweets
            try:
                retweet_button = element.find_element(By.CSS_SELECTOR, '[data-testid="retweet"]')
                retweet_text = retweet_button.get_attribute('aria-label') or retweet_button.text
                metrics['retweets'] = self._parse_number(retweet_text)
            except:
                pass
            
            # Replies
            try:
                reply_button = element.find_element(By.CSS_SELECTOR, '[data-testid="reply"]')
                reply_text = reply_button.get_attribute('aria-label') or reply_button.text
                metrics['replies'] = self._parse_number(reply_text)
            except:
                pass
            
            # Views (if available)
            try:
                view_elements = element.find_elements(By.CSS_SELECTOR, 'span')
                for elem in view_elements:
                    text = elem.text
                    if 'views' in text.lower() or 'K' in text or 'M' in text:
                        metrics['views'] = self._parse_number(text)
                        break
            except:
                pass
            
        except Exception as e:
            logger.debug(f"Error extracting metrics: {e}")
        
        return metrics
    
    def _parse_number(self, text: str) -> int:
        """Parse formatted numbers (1.2K, 3.5M, etc.)"""
        if not text:
            return 0
        
        # Remove non-numeric characters except K, M, B, and decimal point
        text = re.sub(r'[^\d.KMB]', '', text.upper())
        
        if not text or text == '':
            return 0
        
        try:
            multiplier = 1
            if 'K' in text:
                multiplier = 1000
                text = text.replace('K', '')
            elif 'M' in text:
                multiplier = 1000000
                text = text.replace('M', '')
            elif 'B' in text:
                multiplier = 1000000000
                text = text.replace('B', '')
            
            return int(float(text) * multiplier)
        except:
            return 0
    
    def get_user_info(self, username: str) -> Dict:
        """Get user profile information"""
        if not self.driver:
            self._init_driver()
        
        url = f"https://twitter.com/{username}"
        
        try:
            self.driver.get(url)
            time.sleep(3)
            
            from selenium.webdriver.common.by import By
            
            info = {
                'username': username,
                'display_name': '',
                'bio': '',
                'followers': 0,
                'following': 0,
                'verified': False
            }
            
            # Get display name
            try:
                name_element = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="UserName"]')
                info['display_name'] = name_element.text.split('\n')[0]
            except:
                pass
            
            # Get bio
            try:
                bio_element = self.driver.find_element(By.CSS_SELECTOR, '[data-testid="UserDescription"]')
                info['bio'] = bio_element.text
            except:
                pass
            
            # Get follower count
            try:
                followers_element = self.driver.find_element(By.XPATH, '//a[contains(@href, "/followers")]//span')
                info['followers'] = self._parse_number(followers_element.text)
            except:
                pass
            
            return info
            
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            return {}
    
    def close(self):
        """Close browser and cleanup"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("WebDriver closed successfully")
            except:
                pass
            self.driver = None


print("Selenium scraper module loaded")
