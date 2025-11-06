"""
Enhanced Sora Image Scraper for Real Scraping
Scrapes top images from https://sora.chatgpt.com/explore
"""
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import re
import os
from urllib.parse import urlparse
from database import Database


class SoraScraperEnhanced:
    def __init__(self):
        self.base_url = "https://sora.chatgpt.com/explore/top"
        self.images = []
        self.driver = None
        self.visited_urls = set()
        self.images_dir = "images"
        
        # Create images directory if it doesn't exist
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)
            print(f"Created directory: {self.images_dir}")
    
    def download_media(self, url, image_id):
        """Download image or video from URL and save locally"""
        try:
            # Determine file extension
            parsed = urlparse(url)
            ext = os.path.splitext(parsed.path)[1]
            if not ext or ext not in ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.webm', '.mov']:
                ext = '.jpg'  # default
            
            filename = f"{image_id}{ext}"
            filepath = os.path.join(self.images_dir, filename)
            
            # Check if already downloaded
            if os.path.exists(filepath):
                print(f"  Already downloaded: {filename}")
                return filepath
            
            # Download the file
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=30, stream=True)
            response.raise_for_status()
            
            # Save to file
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"  ✓ Downloaded: {filename}")
            return filepath
            
        except Exception as e:
            print(f"  ✗ Download failed: {e}")
            return None
        
    def setup_driver(self):
        """Set up Selenium WebDriver with Chrome"""
        chrome_options = Options()
        
        # Comment out headless mode to see what's happening (useful for debugging)
        # chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Use webdriver_manager to automatically download and manage ChromeDriver
        try:
            service = Service(ChromeDriverManager().install())
            return webdriver.Chrome(service=service, options=chrome_options)
        except Exception as e:
            print(f"Error setting up ChromeDriver with webdriver_manager: {e}")
            print("Trying without service (assuming ChromeDriver in PATH)...")
            return webdriver.Chrome(options=chrome_options)
    
    def scrape_images(self, max_images=50, scroll_wait=3):
        """
        Scrape images from Sora explore/top page
        This collects links to individual image pages, then scrapes each one for details
        """
        print(f"Starting scraper for {self.base_url}...")
        
        try:
            self.driver = self.setup_driver()
            print("Opening Sora top images page...")
            self.driver.get(self.base_url)
            
            # Wait for initial page load
            print("Waiting for page to load...")
            time.sleep(5)
            
            # Check if login is required
            current_url = self.driver.current_url.lower()
            if "login" in current_url or "sign" in current_url or "auth" in current_url:
                print("\n" + "="*60)
                print("⚠️  AUTHENTICATION REQUIRED")
                print("="*60)
                print("Sora requires login. Please:")
                print("1. Log in to the page that just opened")
                print("2. Navigate to https://sora.chatgpt.com/explore/top")
                print("3. Press Enter here when ready to continue scraping...")
                print("\nTake your time - there's no timeout!")
                print("="*60)
                try:
                    input()
                except EOFError:
                    print("\nNo input received, checking if page is ready...")
                    time.sleep(2)
            
            # Verify we're on the right page
            print("\nVerifying page loaded correctly...")
            time.sleep(2)
            final_url = self.driver.current_url
            print(f"Current URL: {final_url}")
            
            if "explore" not in final_url:
                print("\n⚠️  Warning: Not on explore page!")
                print("Attempting to navigate to explore/top...")
                self.driver.get(self.base_url)
                time.sleep(5)
            
            # Step 1: Collect image detail page URLs from gallery
            print(f"\nCollecting image links from gallery...")
            image_links = self._collect_image_links(max_images, scroll_wait)
            print(f"Found {len(image_links)} image links to scrape")
            
            # Step 2: Visit each image page and extract detailed metadata
            print(f"\nScraping detailed metadata from each image...")
            for idx, link in enumerate(image_links[:max_images], 1):
                print(f"[{idx}/{min(len(image_links), max_images)}] Scraping: {link}")
                try:
                    image_data = self._scrape_image_details(link)
                    if image_data:
                        self.images.append(image_data)
                        prompt = image_data.get('prompt', 'No prompt')
                        if prompt:
                            print(f"  ✓ Got: {prompt[:60]}...")
                        else:
                            print(f"  ✓ Got image but no prompt")
                    else:
                        print(f"  ✗ Failed to extract data")
                except Exception as e:
                    print(f"  ✗ Error: {str(e)}")
                time.sleep(2)  # Be polite, don't hammer the server
            
            print(f"\n✓ Successfully scraped {len(self.images)} images with full metadata")
            
            if len(self.images) == 0:
                print("\n⚠️  WARNING: No images were successfully scraped!")
                print("This likely means:")
                print("  1. Sora's HTML structure has changed")
                print("  2. The CSS selectors need to be updated")
                print("  3. JavaScript content isn't loading properly")
                print("\nTip: Check the browser window to see what the pages look like")
            
        except Exception as e:
            print(f"Error during scraping: {e}")
            print("\nTroubleshooting tips:")
            print("1. Make sure Chrome and ChromeDriver are installed and compatible")
            print("2. Check if Sora is accessible in your region")
            print("3. Verify you're not being blocked by rate limiting")
            import traceback
            traceback.print_exc()
            
        finally:
            if self.driver:
                self.driver.quit()
        
        return self.images
    
    def _collect_image_links(self, max_links, scroll_wait):
        """Collect links to individual image detail pages from the gallery"""
        links = set()
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_scrolls = 15
        
        # Debug: Save initial page source
        print("\nDebug: Checking page content...")
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        all_links = soup.find_all('a', href=True)
        print(f"Debug: Found {len(all_links)} total <a> tags on the page")
        
        # Show first few hrefs as examples
        if all_links:
            print("Debug: Sample hrefs:")
            for a in all_links[:10]:
                print(f"  - {a['href']}")
        
        while scroll_attempts < max_scrolls and len(links) < max_links:
            # Parse current page
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Look for links matching the pattern /g/gen_*
            # Adjust selector based on actual Sora HTML structure
            for a_tag in soup.find_all('a', href=True):
                href = a_tag['href']
                # Match Sora's generation URL pattern
                if '/g/gen_' in href or '/gen_' in href:
                    # Make absolute URL
                    if href.startswith('/'):
                        full_url = 'https://sora.chatgpt.com' + href
                    elif not href.startswith('http'):
                        full_url = 'https://sora.chatgpt.com/' + href
                    else:
                        full_url = href
                    
                    links.add(full_url)
                    if len(links) >= max_links:
                        break
            
            print(f"  Found {len(links)} links so far...")
            
            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(scroll_wait)
            
            # Check if we've reached the bottom
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("  Reached end of gallery page")
                break
                
            last_height = new_height
            scroll_attempts += 1
        
        return list(links)
    
    def _scrape_image_details(self, url):
        """Scrape detailed metadata from an individual image page"""
        try:
            self.driver.get(url)
            time.sleep(3)  # Wait for page to load fully
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Extract image ID from URL
            image_id = url.split('/')[-1]
            
            # Initialize data structure
            image_data = {
                'id': image_id,
                'url': url,
                'prompt': None,
                'creator': None,
                'creation_date': None,
                'like_count': None,
                'media_url': None,
                'tags': [],
                'source': 'sora'
            }
            
            # Extract the actual image URL from <img alt="Generated image">
            generated_img = soup.find('img', alt='Generated image')
            if generated_img and generated_img.get('src'):
                image_url = generated_img.get('src')
                print(f"  Found image URL: {image_url[:80]}...")
                
                # Download the image
                local_path = self.download_media(image_url, image_id)
                if local_path:
                    image_data['url'] = local_path
                    image_data['local_file'] = local_path
                    image_data['media_url'] = local_path
                else:
                    # Fallback to screenshot if download fails
                    screenshot_path = os.path.join(self.images_dir, f"{image_id}.png")
                    if not os.path.exists(screenshot_path):
                        self.driver.save_screenshot(screenshot_path)
                        print(f"  ✓ Screenshot fallback: {image_id}.png")
                    image_data['url'] = screenshot_path
                    image_data['local_file'] = screenshot_path
                    image_data['media_url'] = screenshot_path
            else:
                # No image found, take screenshot as fallback
                print(f"  No image URL found, taking screenshot...")
                screenshot_path = os.path.join(self.images_dir, f"{image_id}.png")
                if not os.path.exists(screenshot_path):
                    self.driver.save_screenshot(screenshot_path)
                    print(f"  ✓ Screenshot saved: {image_id}.png")
                image_data['url'] = screenshot_path
                image_data['local_file'] = screenshot_path
                image_data['media_url'] = screenshot_path
            
            # Extract prompt - based on actual Sora HTML structure
            # The prompt is in: div.text-token-text-secondary (contains "Prompt") 
            # followed by button.truncate (contains the actual prompt text)
            
            # Method 1: Look for the button next to "Prompt" text
            prompt_label = soup.find('div', string='Prompt')
            if prompt_label:
                # Find the button sibling
                prompt_button = prompt_label.find_next_sibling('button', class_='truncate')
                if prompt_button:
                    image_data['prompt'] = prompt_button.text.strip()
            
            # Method 2: If method 1 fails, try finding any button with truncate class near "Prompt"
            if not image_data['prompt']:
                prompt_container = soup.find('div', string=re.compile(r'Prompt', re.I))
                if prompt_container:
                    # Look for button in parent hierarchy
                    parent = prompt_container.find_parent()
                    if parent:
                        prompt_button = parent.find('button', class_='truncate')
                        if prompt_button:
                            image_data['prompt'] = prompt_button.text.strip()
            
            # Method 3: Fallback to any button.truncate with substantial text
            if not image_data['prompt']:
                buttons = soup.find_all('button', class_='truncate')
                for button in buttons:
                    text = button.text.strip()
                    if text and len(text) > 20:  # Prompts are usually longer
                        image_data['prompt'] = text
                        break
            
            # Extract creator and title - based on actual Sora HTML structure
            # Structure: div > div (contains username link) + div (separator) + div (contains title)
            
            # Method 1: Find the username in an <a> tag with href containing "/explore?user="
            user_link = soup.find('a', href=re.compile(r'/explore\?user='))
            if user_link:
                image_data['creator'] = user_link.text.strip()
            
            # Method 2: Fallback - look for link in text-token-text-secondary or text-token-text-primary
            if not image_data['creator']:
                creator_divs = soup.find_all('div', class_=re.compile(r'text-token-text-(secondary|primary)'))
                for div in creator_divs:
                    link = div.find('a')
                    if link and link.get('href', '').startswith('/explore'):
                        image_data['creator'] = link.text.strip()
                        break
            
            # Extract title - it's in a div.truncate after the username section
            # Look for div with class "truncate" that contains text (not a button)
            title_candidates = soup.find_all('div', class_='truncate')
            for candidate in title_candidates:
                # Skip if it's a button (that's the prompt)
                if candidate.find_parent('button'):
                    continue
                text = candidate.text.strip()
                # Remove "Prompt" prefix if it exists (sometimes the title includes it)
                if text.startswith('Prompt'):
                    text = text[6:].strip()
                # Title should be reasonable length and not be the username or prompt
                if text and len(text) > 3 and text != image_data.get('creator') and text != image_data.get('prompt'):
                    # Store as a tag or metadata (we'll add title field if needed)
                    if 'title' not in image_data:
                        image_data['title'] = text
                    break
            
            # Extract like count - based on actual Sora HTML structure
            # The like count is in a button with an SVG heart icon
            # Structure: button > div > svg (heart icon) + div (contains the number)
            
            # Method 1: Find button with SVG heart path, then get adjacent div with number
            heart_svg = soup.find('svg', {'viewBox': '0 0 24 24'})
            if heart_svg:
                heart_path = heart_svg.find('path', {'stroke': 'currentColor'})
                if heart_path and 'M12 5.822c6.504' in heart_path.get('d', ''):
                    # Found the heart icon, now find the number in the sibling div
                    button = heart_svg.find_parent('button')
                    if button:
                        like_div = button.find('div', class_='flex px-2 text-center')
                        if like_div:
                            try:
                                image_data['like_count'] = int(like_div.text.strip())
                            except (ValueError, AttributeError):
                                pass
            
            # Method 2: Fallback - look for button with heart SVG and extract any numbers
            if not image_data['like_count']:
                like_buttons = soup.find_all('button', class_=re.compile(r'surface-nav-element'))
                for button in like_buttons:
                    if button.find('svg'):
                        # Check if there's a span or div with "Like" text
                        like_text_elem = button.find('span', class_='sr-only', string=re.compile(r'Like', re.I))
                        if like_text_elem:
                            # Extract number from button text
                            numbers = re.findall(r'\d+', button.text)
                            if numbers:
                                image_data['like_count'] = int(numbers[0])
                                break
            
            # Extract date
            date_elem = soup.find(['time', 'span', 'div'], class_=re.compile(r'(date|time|created)', re.I))
            if date_elem:
                image_data['creation_date'] = date_elem.get('datetime') or date_elem.text.strip()
            
            # Extract tags from prompt
            if image_data['prompt']:
                image_data['tags'] = self._extract_tags_from_text(image_data['prompt'])
            
            return image_data
            
        except Exception as e:
            print(f"  Error scraping {url}: {e}")
            return None
    
    def _extract_tags_from_text(self, text):
        """Extract relevant tags from prompt text"""
        tags = []
        
        if not text:
            return tags
        
        # Keywords that might indicate people in images
        people_keywords = [
            'person', 'people', 'man', 'woman', 'child', 'boy', 'girl',
            'human', 'portrait', 'face', 'family', 'group', 'crowd',
            'individual', 'someone', 'figure', 'character', 'lady', 'gentleman',
            'adult', 'teenager', 'elder', 'senior', 'youth', 'baby', 'infant'
        ]
        
        text_lower = text.lower()
        for keyword in people_keywords:
            if re.search(r'\b' + keyword + r'\b', text_lower):
                tags.append(keyword)
        
        return list(set(tags))  # Remove duplicates
    
    def filter_images_with_people(self):
        """Filter images that likely contain people"""
        filtered = []
        
        for image in self.images:
            # Check if any people-related tags exist
            if image.get('tags'):
                filtered.append(image)
            # Also check the prompt for people keywords
            elif image.get('prompt'):
                people_tags = self._extract_tags_from_text(image['prompt'])
                if people_tags:
                    image['tags'] = people_tags
                    filtered.append(image)
        
        print(f"Filtered to {len(filtered)} images with people")
        return filtered
    
    def save_to_json(self, filename='scraped_images.json'):
        """Save scraped images to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.images, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(self.images)} images to {filename}")
    
    def save_to_database(self, images=None):
        """Save images directly to database (only new ones)"""
        if images is None:
            images = self.images
        
        db = Database()
        
        # Check which images already exist
        conn = db.get_connection()
        cursor = conn.cursor()
        
        existing_ids = set()
        cursor.execute('SELECT id FROM images')
        for row in cursor.fetchall():
            existing_ids.add(row['id'])
        
        conn.close()
        
        # Filter out images that already exist
        new_images = [img for img in images if img['id'] not in existing_ids]
        
        if not new_images:
            print("No new images to add (all already in database)")
            return 0
        
        print(f"Found {len(new_images)} new images out of {len(images)} scraped")
        count = db.add_images(new_images)
        print(f"Added {count} new images to database")
        return count
        return count


def main():
    """Main scraping workflow"""
    print("\n" + "="*60)
    print("Sora Image Scraper")
    print("="*60)
    print("\nThis scraper will attempt to scrape images from Sora.")
    print("Requirements:")
    print("  - Chrome browser installed")
    print("  - ChromeDriver installed (compatible with your Chrome version)")
    print("  - May require Sora account login")
    print("\n" + "="*60 + "\n")
    
    # Get user preferences
    max_images = input("How many images to scrape? (default: 50): ").strip()
    max_images = int(max_images) if max_images.isdigit() else 50
    
    # Initialize scraper
    scraper = SoraScraperEnhanced()
    
    # Scrape images
    all_images = scraper.scrape_images(max_images=max_images)
    
    if not all_images:
        print("\n⚠️  No images found. This could be because:")
        print("  - Sora's HTML structure has changed")
        print("  - Authentication is required")
        print("  - Rate limiting or blocking")
        print("\nYou can still use the mock data for testing.")
        return
    
    print(f"\nTotal images scraped: {len(all_images)}")
    
    # Filter for images with people
    filtered = scraper.filter_images_with_people()
    
    # Save results
    print("\n" + "="*60)
    print("Saving results...")
    print("="*60)
    
    # Always save all images to JSON (for debugging)
    print(f"\nSaving {len(all_images)} images to scraped_images.json...")
    scraper.save_to_json('scraped_images.json')
    
    if filtered:
        print(f"Saving {len(filtered)} filtered images (with people) to scraped_images_people.json...")
        scraper.images = filtered  # Temporarily swap
        scraper.save_to_json('scraped_images_people.json')
        scraper.images = all_images  # Restore
    
    # Ask if user wants to import to database
    response = input("\nImport these images to the database? (y/n): ").strip().lower()
    if response == 'y':
        images_to_import = filtered if filtered else all_images
        print(f"\nImporting {len(images_to_import)} images...")
        count = scraper.save_to_database(images_to_import)
        print(f"\n✓ Successfully imported {count} new images to database!")
        print("\nYou can now run the app with: python app.py")
    else:
        print("\nImages saved to scraped_images.json")
        print("You can import them later using add_images.py")


if __name__ == "__main__":
    main()
