"""
Script to add images to the database
"""
from database import Database

# Initialize database
db = Database()

# Your images - replace with actual image URLs and data
images_to_add = [
    {
        'id': 'custom_1',
        'url': 'https://your-image-url-here.com/image1.jpg',
        'prompt': 'Description of the image or prompt used to generate it',
        'tags': ['person', 'woman', 'portrait'],
        'source': 'custom'
    },
    {
        'id': 'custom_2',
        'url': 'https://your-image-url-here.com/image2.jpg',
        'prompt': 'Another description',
        'tags': ['people', 'group', 'family'],
        'source': 'custom'
    },
    # Add more images here...
]

# Add images to database
count = db.add_images(images_to_add)
print(f"Successfully added {count} images to the database")

# Optional: Check statistics
stats = db.get_statistics()
print(f"\nTotal images in database: {stats['total_images']}")
