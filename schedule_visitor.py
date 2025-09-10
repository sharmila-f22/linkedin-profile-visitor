import time
import random
import os
import subprocess
import json
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv


load_dotenv(override=True)


# Function to initialize the driver
def setup_driver():
    """Setup Chrome driver and return the driver instance."""
    print("Initializing the Chrome driver...")
    
    # Setup Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    # chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    # chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    # chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    # chrome_options.add_argument("--window-size=1920,1080")  # Set window size for headless mode
    # chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")  # Set realistic user agent
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver


# Function to add the LinkedIn cookie
def add_cookie(driver):
    """Add the LinkedIn session cookie to the browser (simplified version)."""
    print("Adding LinkedIn session cookie...")
    
    # Ensure we're on LinkedIn
    driver.get("https://www.linkedin.com")
    time.sleep(2)
    
    cookie_file = os.getenv("COOKIES_PATH")
    with open(cookie_file, 'r') as file:
        cookies = json.load(file)
    
    for cookie in cookies:
        try:
            # Only add essential cookie data
            cookie_data = {
                'name': cookie["name"],
                'value': cookie["value"],
                'domain': '.linkedin.com',  # Force LinkedIn domain
                'path': '/'
            }
            
            driver.add_cookie(cookie_data)
            print(f"✅ Added cookie: {cookie['name']}")
            
        except Exception as e:
            print(f"⚠️ Failed to add cookie {cookie.get('name', 'unknown')}: {e}")
            continue
    
    driver.refresh()
    time.sleep(2)
    print("✅ Logged in using cookies!")


# Function to visit a single profile
def visit_profile(url):
    """Visit a single LinkedIn profile URL."""
    print(f"Visiting profile: {url}")
    driver = None
    try:
        driver = setup_driver()  # Initialize the driver for each job

        # Test bot detection
        driver.get("https://bot.sannysoft.com/")
        time.sleep(2)
        
        # Add the LinkedIn cookie
        add_cookie(driver)
        
        # Visit the profile
        driver.get(url)

        wait_time = round(random.uniform(5, 10), 1)  # Random float with 1 decimal place
        print(f"   Waiting for {wait_time} seconds...")
        time.sleep(wait_time)

        print(f"   ✅ Successfully visited: {url}")
    except Exception as e:
        print(f"   ❌ Error visiting {url}: {e}")
    finally:
        # Close the browser and cleanup
        if driver:
            try:
                print("Closing the browser...")
                driver.quit()
                print("✅ Browser closed.")
            except Exception as e:
                print(f"⚠️ Error closing browser: {e}")
                # Force kill Chrome processes if quit fails
                try:
                    subprocess.run(['pkill', '-f', 'chromium'], check=False)
                except:
                    pass


# Function to load profile URLs from environment variable
def load_profile_urls():
    """Load LinkedIn profile URLs from environment variable."""
    try:
        urls = os.getenv("URLS")
        urls_json = json.loads(urls)
        print(f"✅ Loaded {len(urls_json['urls'])} profile URLs.")
        return urls_json["urls"]
    except Exception as e:
        print(f"❌ Error loading URLs: {e}")
        return []


# Main function
def main():
    print("🎯 Starting main function...")
        # Load profile URLs
    profile_urls = load_profile_urls()
    if not profile_urls:
        print("❌ No valid profile URLs found. Exiting...")
        return


    print(f"📅 Current time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        # Schedule a job for each URL
    for index, url in enumerate(profile_urls):
        # Schedule each job at a specific time
        schedule_time = "13:39"  # Change this to your desired time
        print(f"⏰ Scheduling job for URL {index + 1} at {schedule_time}: {url}")
        # schedule.every().day.at(schedule_time).do(visit_profile, url)
        # schedule.every(1).minutes.do(visit_profile, url)
        visit_profile(url)


    print("✅ Scheduler is running. Jobs are scheduled for each URL.")
    print("⏳ Waiting for scheduled time...")


    # Keep the script running to allow the scheduler to execute the jobs
    while True:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        print(f"🕐 Current time: {current_time}")
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()




