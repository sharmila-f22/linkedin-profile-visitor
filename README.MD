# LinkedIn Profile Visitor

An automated LinkedIn profile visitor that uses Selenium WebDriver to visit LinkedIn profiles on a scheduled basis. This tool helps you maintain visibility and engagement on LinkedIn by automatically visiting profiles at specified intervals.


## Features

- �� Automated LinkedIn profile visiting using Selenium WebDriver
- ⏰ Scheduled profile visits with configurable timing
- �� Session management using saved cookies
- 🔄 Random wait times to simulate human behavior
- 📊 Support for multiple profile URLs
- 🛡️ Bot detection testing capabilities

## Prerequisites

- Python 3.7+
- Chrome/Chromium browser
- ChromeDriver (automatically managed by Selenium)
- LinkedIn account with valid session cookies

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd linkedin_profile_visitor
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Path to your LinkedIn session cookies JSON file
COOKIES_PATH=./cookies.json

# LinkedIn profile URLs to visit (JSON format)
URLS={"urls": ["https://linkedin.com/in/profile1", "https://linkedin.com/in/profile2"]}
```

### Cookie Setup

1. **Export LinkedIn cookies:**
   - Log into LinkedIn in your browser
   - Use browser developer tools or a cookie export extension eg: editThisCookie
   - Export cookies as JSON format
   - Save as `cookies.json` in the project root

2. **Cookie format example:**
   ```json
   [
     {
       "name": "li_at",
       "value": "your_session_token_here",
       "domain": ".linkedin.com",
       "path": "/"
     }
   ]
   ```

## Usage

### Basic Usage

1. **Configure your environment variables** in `.env`
2. **Add your LinkedIn cookies** to `cookies.json`
3. **Run the script:**
   ```bash
   python schedule_visitor
   ```

### Scheduling Options

To modify the schedule:

```python
# In schedule_visitor file, line 207:
schedule.every(1).minutes.do(visit_profile, url)  # Every minute
schedule.every().day.at("13:39").do(visit_profile, url)  # Daily at specific time
schedule.every(2).hours.do(visit_profile, url)  # Every 2 hours
```