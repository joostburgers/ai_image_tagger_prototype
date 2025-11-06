"""
Sora Image Scraper
Scrapes top images from https://sora.chatgpt.com/explore
"""
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json


class SoraScraper:
    def __init__(self):
        self.base_url = "https://sora.chatgpt.com/explore"
        self.images = []
        
    def setup_driver(self):
        """Set up Selenium WebDriver with headless Chrome"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        return webdriver.Chrome(options=chrome_options)
    
    def scrape_images(self, max_images=50):
        """
        Scrape images from Sora explore page
        Note: This is a mockup implementation. The actual Sora site may require
        authentication and have dynamic loading that needs specific handling.
        """
        print(f"Scraping images from {self.base_url}...")
        
        try:
            driver = self.setup_driver()
            driver.get(self.base_url)
            
            # Wait for page to load (adjust selector based on actual site structure)
            time.sleep(3)  # Simple wait; in production, use WebDriverWait
            
            # Scroll to load more images if needed
            last_height = driver.execute_script("return document.body.scrollHeight")
            scroll_attempts = 0
            max_scrolls = 5
            
            while scroll_attempts < max_scrolls:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                
                if new_height == last_height:
                    break
                    
                last_height = new_height
                scroll_attempts += 1
            
            # Parse the page
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Find image elements (selectors will need to be adjusted for actual site)
            # This is a generic approach that looks for common image patterns
            image_containers = soup.find_all(['img', 'video', 'figure', 'div'], limit=max_images)
            
            for idx, container in enumerate(image_containers[:max_images]):
                image_data = self._extract_image_data(container, idx)
                if image_data:
                    self.images.append(image_data)
            
            driver.quit()
            print(f"Successfully scraped {len(self.images)} images")
            
        except Exception as e:
            print(f"Error scraping images: {e}")
            print("Note: This scraper may need adjustment based on Sora's actual structure")
        
        return self.images
    
    def _extract_image_data(self, element, idx):
        """Extract image URL and tags from an element"""
        image_data = {
            'id': f"sora_{idx}_{int(time.time())}",
            'url': None,
            'prompt': None,
            'tags': [],
            'source': 'sora'
        }
        
        # Try to find image URL
        if element.name == 'img':
            image_data['url'] = element.get('src') or element.get('data-src')
        elif element.name == 'video':
            image_data['url'] = element.get('poster') or element.get('src')
        else:
            img_tag = element.find('img')
            if img_tag:
                image_data['url'] = img_tag.get('src') or img_tag.get('data-src')
        
        # Try to find prompt/caption
        caption_tags = ['figcaption', 'p', 'span']
        for tag in caption_tags:
            caption = element.find(tag)
            if caption and caption.text.strip():
                image_data['prompt'] = caption.text.strip()
                break
        
        # Extract tags from prompt or metadata
        if image_data['prompt']:
            image_data['tags'] = self._extract_tags_from_text(image_data['prompt'])
        
        # Only return if we found an image URL
        if image_data['url']:
            return image_data
        
        return None
    
    def _extract_tags_from_text(self, text):
        """Extract relevant tags from prompt text"""
        tags = []
        
        # Keywords that might indicate people in images
        people_keywords = [
            'person', 'people', 'man', 'woman', 'child', 'boy', 'girl',
            'human', 'portrait', 'face', 'family', 'group', 'crowd',
            'individual', 'someone', 'figure', 'character'
        ]
        
        text_lower = text.lower()
        for keyword in people_keywords:
            if keyword in text_lower:
                tags.append(keyword)
        
        return list(set(tags))  # Remove duplicates
    
    def filter_images_with_people(self):
        """Filter images that likely contain people"""
        filtered = []
        
        for image in self.images:
            # Check if any people-related tags exist
            if image['tags']:
                filtered.append(image)
            # Also check the prompt for people keywords
            elif image['prompt']:
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


def get_mock_data():
    """
    Generate mock data for development/testing
    Use this when you can't access the actual Sora site
    """
    mock_images = [
        {
            'id': 'mock_1',
            'url': 'https://via.placeholder.com/800x600/4A90E2/FFFFFF?text=AI+Generated+Portrait+1',
            'prompt': 'A professional portrait of a young woman in a business suit',
            'tags': ['person', 'woman', 'portrait'],
            'source': 'mock'
        },
        {
            'id': 'mock_2',
            'url': 'https://via.placeholder.com/800x600/E94B3C/FFFFFF?text=AI+Generated+Group+2',
            'prompt': 'A diverse group of people collaborating in an office',
            'tags': ['people', 'group'],
            'source': 'mock'
        },
        {
            'id': 'mock_3',
            'url': 'https://via.placeholder.com/800x600/6AB04C/FFFFFF?text=AI+Generated+Family+3',
            'prompt': 'A happy family having dinner together',
            'tags': ['people', 'family'],
            'source': 'mock'
        },
        {
            'id': 'mock_4',
            'url': 'https://via.placeholder.com/800x600/F8B500/FFFFFF?text=AI+Generated+Elder+4',
            'prompt': 'An elderly man reading a book in a library',
            'tags': ['person', 'man'],
            'source': 'mock'
        },
        {
            'id': 'mock_5',
            'url': 'https://via.placeholder.com/800x600/9B59B6/FFFFFF?text=AI+Generated+Child+5',
            'prompt': 'A young child playing in a park',
            'tags': ['child', 'person'],
            'source': 'mock'
        },
    ]
    
    return mock_images


if __name__ == "__main__":
    # For development, use mock data
    print("Running in mock mode...")
    images = get_mock_data()
    
    with open('scraped_images.json', 'w', encoding='utf-8') as f:
        json.dump(images, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(images)} mock images")
    
    # To use real scraper (requires Chrome driver and may need adjustments):
    # scraper = SoraScraper()
    # scraper.scrape_images(max_images=50)
    # filtered = scraper.filter_images_with_people()
    # scraper.save_to_json()
