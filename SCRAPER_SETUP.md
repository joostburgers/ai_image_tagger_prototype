# Sora Scraper Setup Guide

## Prerequisites

### 1. Install ChromeDriver

**Option A: Automatic (Recommended)**
```powershell
pip install webdriver-manager
```

Then the scraper will auto-download the correct driver.

**Option B: Manual Install**
1. Check your Chrome version: Open Chrome → Help → About Google Chrome
2. Download matching ChromeDriver from: https://chromedriver.chromium.org/downloads
3. Extract and add to PATH, or place in project folder

### 2. Verify Installation

```powershell
# Test if Chrome can be found
python -c "from selenium import webdriver; driver = webdriver.Chrome(); driver.quit(); print('ChromeDriver works!')"
```

## Running the Scraper

### Basic Usage

```powershell
python scraper_enhanced.py
```

The scraper will:
1. Open Chrome browser (you'll see it)
2. Navigate to Sora explore page
3. If login required, pause for you to log in
4. Scroll and collect images
5. Filter for images with people
6. Save to JSON and optionally import to database

### Configuration

Edit these parameters in `scraper_enhanced.py`:

- `max_images`: Number of images to scrape (default: 50)
- `scroll_wait`: Seconds to wait between scrolls (default: 3)
- Enable headless mode: Uncomment line 30 in `setup_driver()`

## Troubleshooting

### "ChromeDriver not found"
- Install ChromeDriver or use webdriver-manager
- Make sure it's in your PATH or project directory

### "Login required" 
- Scraper will pause for you to log in manually
- Navigate to explore page after login
- Press Enter in terminal to continue

### "No images found"
- Sora's HTML structure may have changed
- Check if site is accessible in your region
- Try running with headless mode disabled (comment line 30)
- Inspect the page source to find correct selectors

### Rate Limiting
- Increase `scroll_wait` time
- Reduce `max_images`
- Add delays between scraping sessions

## Alternative: Using Mock Data

If scraping doesn't work, you can still develop with mock data:

```powershell
python scraper.py
```

This generates placeholder images for testing.

## Customizing Selectors

If Sora's structure changed, update these in `_extract_images_from_page()`:

```python
# Look for specific classes or IDs from Sora's actual HTML
videos = soup.find_all('video', class_='actual-class-name')
containers = soup.find_all('div', class_='sora-card-class')
```

Use browser DevTools (F12) to inspect Sora's actual HTML structure.
