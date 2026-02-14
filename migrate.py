"""
Database Migration Script
Adds the 'score' column to the submit_assessment table
Run this ONCE before starting the application
"""

import sqlite3
import os

# Path to your database file
DB_PATH = 'instance/submit-assessment.db'

def migrate_database():
    """Add score column to submit_assessment table if it doesn't exist"""
    
    # Check if database exists
    if not os.path.exists(DB_PATH):
        print(f" Database not found at {DB_PATH}")
        print("The database will be created automatically when you run the app.")
        return
    
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if score column already exists
        cursor.execute("PRAGMA table_info(submit_assessment)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'score' in columns:
            print("Score column already exists. No migration needed.")
            conn.close()
            return
        
        # Add the score column
        print("Adding 'score' column to submit_assessment table...")
        cursor.execute("ALTER TABLE submit_assessment ADD COLUMN score INTEGER")
        
        # Calculate and update scores for existing records
        print("Calculating scores for existing assessments...")
        
        # Fetch all existing records
        cursor.execute("SELECT id, q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11, q12, q13, q14, q15, q16, q17, q18, q19, q20 FROM submit_assessment")
        records = cursor.fetchall()
        
        # Score mappings (same as in app.py)
        score_mappings = [
            {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}, {1: 5, 2: 4, 3: 3, 4: 2, 5: 1},
            {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5},
            {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5},
            {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5},
            {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, {1: 5, 2: 4, 3: 3, 4: 2, 5: 1},
            {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5},
            {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5},
            {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5},
            {1: 5, 2: 4, 3: 3, 4: 2, 5: 1}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5},
            {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}, {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
        ]
        
        updated_count = 0
        for record in records:
            record_id = record[0]
            answers = record[1:]  # q1 to q20
            
            # Calculate score
            total_score = 0
            for i, answer in enumerate(answers):
                if answer is not None:
                    total_score += score_mappings[i].get(answer, 0)
            
            # Update the record
            cursor.execute("UPDATE submit_assessment SET score = ? WHERE id = ?", (total_score, record_id))
            updated_count += 1
        
        conn.commit()
        print(f" Successfully migrated database!")
        print(f"   - Added 'score' column")
        print(f"   - Updated {updated_count} existing records with calculated scores")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f" Database error: {e}")
    except Exception as e:
        print(f" Unexpected error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Youth Connect Hub - Database Migration")
    print("=" * 60)
    print()
    
    migrate_database()
    
    print()
    print("=" * 60)
    print("Migration complete! You can now start your Flask app.")
    print("=" * 60)