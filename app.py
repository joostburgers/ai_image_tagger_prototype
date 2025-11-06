"""
Flask Web Application for AI Image Bias Tagger
"""
from flask import Flask, render_template, request, jsonify, session, send_from_directory
from flask_cors import CORS
import os
import secrets
from database import Database
from scraper import get_mock_data
import json

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', secrets.token_hex(32))
CORS(app)

# Initialize database
db = Database()


@app.route('/images/<path:filename>')
def serve_image(filename):
    """Serve images from the images directory"""
    return send_from_directory('images', filename)


@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/tag')
def tag_page():
    """Image tagging page"""
    # Create or get user session
    if 'user_id' not in session:
        session['user_id'] = secrets.token_hex(16)
        db.create_or_get_session(session['user_id'])
    
    return render_template('tag.html')


@app.route('/api/next-image')
def get_next_image():
    """API endpoint to get the next image for tagging"""
    if 'user_id' not in session:
        session['user_id'] = secrets.token_hex(16)
        db.create_or_get_session(session['user_id'])
    
    user_id = session['user_id']
    image = db.get_random_unviewed_image(user_id)
    
    if not image:
        return jsonify({'error': 'No more images available', 'has_more': False}), 404
    
    # Record the view
    db.record_view(image['id'], user_id)
    
    # Parse tags if they're stored as JSON
    if image['tags']:
        try:
            image['tags'] = json.loads(image['tags'])
        except (json.JSONDecodeError, TypeError):
            image['tags'] = []
    
    return jsonify({
        'image': image,
        'has_more': True
    })


@app.route('/api/submit-tags', methods=['POST'])
def submit_tags():
    """API endpoint to submit bias tags for an image"""
    data = request.json
    
    if 'user_id' not in session:
        return jsonify({'error': 'No session found'}), 403
    
    image_id = data.get('image_id')
    bias_tags = data.get('bias_tags', [])
    notes = data.get('notes', '')
    
    if not image_id:
        return jsonify({'error': 'Image ID required'}), 400
    
    user_id = session['user_id']
    
    # Add each bias tag
    success = True
    for bias_type in bias_tags:
        if not db.add_bias_tag(image_id, user_id, bias_type, notes):
            success = False
    
    if success:
        return jsonify({'success': True, 'message': 'Tags submitted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Error submitting some tags'}), 500


@app.route('/api/skip-image', methods=['POST'])
def skip_image():
    """API endpoint to skip an image without tagging"""
    data = request.json
    
    if 'user_id' not in session:
        return jsonify({'error': 'No session found'}), 403
    
    image_id = data.get('image_id')
    
    if not image_id:
        return jsonify({'error': 'Image ID required'}), 400
    
    # View is already recorded when image was fetched
    return jsonify({'success': True, 'message': 'Image skipped'})


@app.route('/dashboard')
def dashboard():
    """Statistics dashboard page"""
    return render_template('dashboard.html')


@app.route('/api/statistics')
def get_statistics():
    """API endpoint to get statistics"""
    stats = db.get_statistics()
    return jsonify(stats)


@app.route('/api/load-mock-data', methods=['POST'])
def load_mock_data():
    """API endpoint to load mock data for testing"""
    try:
        mock_images = get_mock_data()
        added = db.add_images(mock_images)
        return jsonify({
            'success': True,
            'message': f'Loaded {added} mock images',
            'count': added
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading mock data: {str(e)}'
        }), 500


@app.route('/about')
def about():
    """About page explaining the project"""
    return render_template('about.html')


if __name__ == '__main__':
    # Load initial data if database is empty
    stats = db.get_statistics()
    if stats['total_images'] == 0:
        print("Database is empty. Attempting to load scraped images...")
        
        # Try to load scraped images first
        try:
            import os.path
            if os.path.exists('scraped_images_people.json'):
                with open('scraped_images_people.json', 'r') as f:
                    scraped_data = json.load(f)
                    if scraped_data:
                        print(f"Loading {len(scraped_data)} scraped images...")
                        db.add_images(scraped_data)
                        print("✓ Scraped images loaded successfully!")
                    else:
                        raise ValueError("Scraped images file is empty")
            else:
                raise FileNotFoundError("No scraped images found")
        except Exception as e:
            print(f"Could not load scraped images: {e}")
            print("Loading mock data instead...")
            mock_images = get_mock_data()
            db.add_images(mock_images)
    
    # Get port from environment variable (for cloud deployment)
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    
    print("\n" + "="*60)
    print("AI Image Bias Tagger - Development Server")
    print("="*60)
    print(f"\nServer starting at http://localhost:{port}")
    print("\nAvailable pages:")
    print(f"  - Home: http://localhost:{port}/")
    print(f"  - Tagging Interface: http://localhost:{port}/tag")
    print(f"  - Dashboard: http://localhost:{port}/dashboard")
    print(f"  - About: http://localhost:{port}/about")
    print("\nPress Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
