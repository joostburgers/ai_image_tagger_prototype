"""
Generate scraped_images_people.json from local images
"""
import os
import json
import random

def generate_image_data():
    """Generate JSON data for all images in the images folder"""
    images_dir = 'images'
    image_files = [f for f in os.listdir(images_dir) if f.endswith(('.jpg', '.jpeg', '.png', '.webp'))]
    
    # Sample prompts for variety
    prompts = [
        "A professional portrait in a modern office setting",
        "A diverse group of people collaborating on a project",
        "A candid street photography scene with pedestrians",
        "A formal business meeting with executives",
        "A casual gathering of friends at a cafe",
        "A family portrait in a park setting",
        "A student studying in a university library",
        "A healthcare worker in a medical facility",
        "An artist working in their studio",
        "A chef preparing food in a restaurant kitchen",
        "A teacher instructing students in a classroom",
        "A scientist conducting research in a laboratory",
        "A musician performing on stage",
        "An athlete training at a gym",
        "A construction worker at a building site",
        "A retail worker assisting customers",
        "A photographer taking pictures at an event",
        "A couple walking in an urban environment",
        "Children playing at a playground",
        "Elderly people enjoying a community center",
        "Young professionals networking at a conference",
        "A fashion model posing for a photoshoot",
        "A barista making coffee at a cafe",
        "A delivery person making a drop-off",
        "A security guard monitoring an area",
    ]
    
    # Sample tags
    tag_options = [
        ['person', 'portrait'],
        ['people', 'group'],
        ['man', 'professional'],
        ['woman', 'portrait'],
        ['family', 'people'],
        ['child', 'person'],
        ['individual', 'portrait'],
        ['crowd', 'people'],
        ['figure', 'human'],
        ['character', 'person'],
    ]
    
    image_data = []
    
    for idx, filename in enumerate(image_files):
        # Create image entry
        entry = {
            'id': f'gen_{idx:04d}',
            'url': f'/images/{filename}',
            'prompt': random.choice(prompts),
            'tags': random.choice(tag_options),
            'source': 'local'
        }
        image_data.append(entry)
    
    # Save to JSON file
    output_file = 'scraped_images_people.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(image_data, f, indent=2, ensure_ascii=False)
    
    print(f"✓ Generated {len(image_data)} image entries")
    print(f"✓ Saved to {output_file}")
    return len(image_data)

if __name__ == '__main__':
    generate_image_data()
