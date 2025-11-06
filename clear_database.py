"""
Clear/reset the database
"""
from database import Database
import os

def clear_database():
    """Clear all data from the database"""
    db = Database()
    conn = db.get_connection()
    cursor = conn.cursor()
    
    print("Clearing database...")
    
    # Delete all records from tables (keeps table structure)
    cursor.execute('DELETE FROM image_views')
    cursor.execute('DELETE FROM bias_tags')
    cursor.execute('DELETE FROM images')
    cursor.execute('DELETE FROM user_sessions')
    
    conn.commit()
    conn.close()
    
    print("✓ Database cleared successfully")
    print("All images, tags, views, and sessions have been removed")

def delete_database():
    """Delete the entire database file"""
    db_path = 'data/bias_tagger.db'
    
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✓ Database file deleted: {db_path}")
        print("A new database will be created next time you run the app")
    else:
        print(f"Database file not found: {db_path}")

if __name__ == "__main__":
    print("\nDatabase Reset Options:")
    print("1. Clear all data (keeps database structure)")
    print("2. Delete database file completely")
    print("3. Cancel")
    
    choice = input("\nChoose an option (1-3): ").strip()
    
    if choice == "1":
        clear_database()
    elif choice == "2":
        confirm = input("Are you sure? This will delete the entire database (y/n): ").strip().lower()
        if confirm == 'y':
            delete_database()
        else:
            print("Cancelled")
    else:
        print("Cancelled")
