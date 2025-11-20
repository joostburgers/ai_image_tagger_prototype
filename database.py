"""
Database models and setup for AI Image Bias Tagger
"""
import sqlite3
from datetime import datetime
import json
import os


class Database:
    def __init__(self, db_path='data/bias_tagger.db'):
        self.db_path = db_path
        
        # Create data directory if it doesn't exist
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self.init_database()
    
    def get_connection(self):
        """Get a database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return conn
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Images table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id TEXT PRIMARY KEY,
                url TEXT NOT NULL,
                prompt TEXT,
                tags TEXT,
                source TEXT,
                view_count INTEGER DEFAULT 0,
                unique_viewers INTEGER DEFAULT 0,
                bias_tag_count INTEGER DEFAULT 0,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                deleted_at TIMESTAMP NULL
            )
        ''')
        
        # Bias tags table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bias_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_id TEXT NOT NULL,
                user_session TEXT NOT NULL,
                bias_type TEXT NOT NULL,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (image_id) REFERENCES images(id),
                UNIQUE(image_id, user_session, bias_type)
            )
        ''')
        
        # User sessions table (to track unique viewers)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_id TEXT PRIMARY KEY,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Image views table (to track who viewed what)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS image_views (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_id TEXT NOT NULL,
                user_session TEXT NOT NULL,
                viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (image_id) REFERENCES images(id),
                FOREIGN KEY (user_session) REFERENCES user_sessions(session_id),
                UNIQUE(image_id, user_session)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_images_status ON images(status)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_bias_tags_image ON bias_tags(image_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_image_views_session ON image_views(user_session)')
        
        conn.commit()
        conn.close()
        
        print("Database initialized successfully")
    
    def add_images(self, images_data):
        """Add multiple images to the database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        added_count = 0
        for img in images_data:
            try:
                cursor.execute('''
                    INSERT OR IGNORE INTO images (id, url, prompt, tags, source)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    img['id'],
                    img['url'],
                    img.get('prompt', ''),
                    json.dumps(img.get('tags', [])),
                    img.get('source', 'unknown')
                ))
                if cursor.rowcount > 0:
                    added_count += 1
            except Exception as e:
                print(f"Error adding image {img.get('id')}: {e}")
        
        conn.commit()
        conn.close()
        
        print(f"Added {added_count} new images to database")
        return added_count
    
    def get_random_unviewed_image(self, session_id):
        """Get a random image that this user hasn't viewed yet"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT i.* FROM images i
            WHERE i.status = 'active'
            AND i.id NOT IN (
                SELECT image_id FROM image_views
                WHERE user_session = ?
            )
            ORDER BY RANDOM()
            LIMIT 1
        ''', (session_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def record_view(self, image_id, session_id):
        """Record that a user viewed an image"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Add view record
            cursor.execute('''
                INSERT OR IGNORE INTO image_views (image_id, user_session)
                VALUES (?, ?)
            ''', (image_id, session_id))
            
            # Update image view count
            cursor.execute('''
                UPDATE images
                SET view_count = view_count + 1,
                    unique_viewers = (
                        SELECT COUNT(DISTINCT user_session)
                        FROM image_views
                        WHERE image_id = ?
                    )
                WHERE id = ?
            ''', (image_id, image_id))
            
            # Check if image should be deleted (5 views, no bias tags)
            cursor.execute('''
                SELECT unique_viewers, bias_tag_count
                FROM images
                WHERE id = ?
            ''', (image_id,))
            
            result = cursor.fetchone()
            if result and result['unique_viewers'] >= 5 and result['bias_tag_count'] == 0:
                cursor.execute('''
                    UPDATE images
                    SET status = 'deleted', deleted_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (image_id,))
                print(f"Image {image_id} marked as deleted (5 views, no bias tags)")
            
            conn.commit()
        except Exception as e:
            print(f"Error recording view: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def add_bias_tag(self, image_id, session_id, bias_type, notes=''):
        """Add a bias tag to an image"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO bias_tags (image_id, user_session, bias_type, notes)
                VALUES (?, ?, ?, ?)
            ''', (image_id, session_id, bias_type, notes))
            
            # Update bias tag count
            cursor.execute('''
                UPDATE images
                SET bias_tag_count = (
                    SELECT COUNT(DISTINCT bias_type)
                    FROM bias_tags
                    WHERE image_id = ?
                )
                WHERE id = ?
            ''', (image_id, image_id))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding bias tag: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
    
    def create_or_get_session(self, session_id):
        """Create or update a user session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_sessions (session_id, last_active)
            VALUES (?, CURRENT_TIMESTAMP)
        ''', (session_id,))
        
        conn.commit()
        conn.close()
    
    def get_statistics(self):
        """Get overall statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total images
        cursor.execute('SELECT COUNT(*) as count FROM images WHERE status = "active"')
        stats['total_images'] = cursor.fetchone()['count']
        
        # Total views
        cursor.execute('SELECT SUM(view_count) as count FROM images')
        stats['total_views'] = cursor.fetchone()['count'] or 0
        
        # Images with bias tags
        cursor.execute('SELECT COUNT(*) as count FROM images WHERE bias_tag_count > 0')
        stats['tagged_images'] = cursor.fetchone()['count']
        
        # Bias type breakdown
        cursor.execute('''
            SELECT bias_type, COUNT(*) as count
            FROM bias_tags
            GROUP BY bias_type
            ORDER BY count DESC
        ''')
        stats['bias_types'] = [dict(row) for row in cursor.fetchall()]
        
        # Recently tagged images
        cursor.execute('''
            SELECT i.id, i.url, i.prompt, 
                   GROUP_CONCAT(DISTINCT bt.bias_type) as bias_types
            FROM images i
            JOIN bias_tags bt ON i.id = bt.image_id
            WHERE i.bias_tag_count > 0
            GROUP BY i.id
            ORDER BY MAX(bt.created_at) DESC
            LIMIT 10
        ''')
        stats['recent_tagged'] = [dict(row) for row in cursor.fetchall()]
        
        # Most tagged image
        cursor.execute('''
            SELECT i.id, i.url, i.prompt, i.bias_tag_count as tag_count,
                   GROUP_CONCAT(DISTINCT bt.bias_type) as bias_types
            FROM images i
            LEFT JOIN bias_tags bt ON i.id = bt.image_id
            WHERE i.bias_tag_count > 0
            GROUP BY i.id
            ORDER BY i.bias_tag_count DESC
            LIMIT 1
        ''')
        most_tagged_row = cursor.fetchone()
        stats['most_tagged'] = dict(most_tagged_row) if most_tagged_row else None
        
        conn.close()
        return stats
    
    def get_image_details(self, image_id):
        """Get detailed information about an image"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get image data
        cursor.execute('SELECT * FROM images WHERE id = ?', (image_id,))
        image = cursor.fetchone()
        
        if not image:
            conn.close()
            return None
        
        image_dict = dict(image)
        
        # Get bias tags
        cursor.execute('''
            SELECT bias_type, COUNT(*) as count
            FROM bias_tags
            WHERE image_id = ?
            GROUP BY bias_type
        ''', (image_id,))
        
        image_dict['bias_tags'] = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return image_dict


if __name__ == "__main__":
    # Test the database
    db = Database()
    print("Database setup complete!")
