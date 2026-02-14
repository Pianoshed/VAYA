"""
Database Table Reset Script
Clears all data from submit_assessment table
WARNING: This will delete ALL assessment data!
"""

import sqlite3
import os
from datetime import datetime

# Path to your database file
DB_PATH = 'instance/submit-assessment.db'

def backup_database():
    """Create a backup before resetting"""
    if os.path.exists(DB_PATH):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f'instance/submit-assessment_backup_{timestamp}.db'
        
        print(f"Creating backup at: {backup_path}")
        
        # Copy database file
        import shutil
        shutil.copy2(DB_PATH, backup_path)
        print(f"SUCCESS: Backup created!")
        return backup_path
    return None

def reset_table():
    """Clear all data from submit_assessment table"""
    
    if not os.path.exists(DB_PATH):
        print("ERROR: Database not found at", DB_PATH)
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Count current records
        cursor.execute("SELECT COUNT(*) FROM submit_assessment")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("Table is already empty!")
            conn.close()
            return True
        
        print(f"Found {count} records in submit_assessment table")
        
        # Confirm deletion
        print("\nWARNING: This will permanently delete all assessment data!")
        confirm = input("Type 'DELETE ALL' to confirm: ")
        
        if confirm != "DELETE ALL":
            print("Reset cancelled.")
            conn.close()
            return False
        
        # Delete all records
        print("\nDeleting all records...")
        cursor.execute("DELETE FROM submit_assessment")
        
        # Reset auto-increment counter
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='submit_assessment'")
        
        conn.commit()
        print(f"SUCCESS: Deleted {count} records!")
        print("Table has been reset. Next ID will be 1.")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def view_table_info():
    """Display current table information"""
    
    if not os.path.exists(DB_PATH):
        print("ERROR: Database not found")
        return
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Count records
        cursor.execute("SELECT COUNT(*) FROM submit_assessment")
        count = cursor.fetchone()[0]
        
        print("\n" + "="*60)
        print("SUBMIT_ASSESSMENT TABLE INFO")
        print("="*60)
        print(f"Total Records: {count}")
        
        if count > 0:
            # Get date range
            cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM submit_assessment")
            min_date, max_date = cursor.fetchone()
            print(f"Date Range: {min_date} to {max_date}")
            
            # Get score stats
            cursor.execute("SELECT AVG(score), MIN(score), MAX(score) FROM submit_assessment WHERE score IS NOT NULL")
            avg, min_score, max_score = cursor.fetchone()
            if avg:
                print(f"Score Range: {min_score} to {max_score} (avg: {round(avg, 2)})")
            
            # Show last 5 records
            cursor.execute("SELECT id, email, score, timestamp FROM submit_assessment ORDER BY id DESC LIMIT 5")
            print("\nLast 5 Records:")
            print("-" * 60)
            for row in cursor.fetchall():
                print(f"ID: {row[0]} | Email: {row[1]} | Score: {row[2]} | Date: {row[3]}")
        else:
            print("Table is empty")
        
        print("="*60 + "\n")
        
        conn.close()
        
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Youth Connect Hub - Table Reset Tool")
    print("=" * 60)
    print()
    
    # Show current table info
    view_table_info()
    
    # Ask what to do
    print("Options:")
    print("1. View table info only")
    print("2. Reset table (with backup)")
    print("3. Reset table (without backup)")
    print("4. Exit")
    print()
    
    choice = input("Enter your choice (1-4): ")
    
    if choice == "1":
        print("\nTable info displayed above.")
    
    elif choice == "2":
        print("\nResetting table with backup...")
        backup_path = backup_database()
        if backup_path:
            print(f"Backup saved to: {backup_path}")
            reset_table()
        else:
            print("ERROR: Could not create backup")
    
    elif choice == "3":
        print("\nWARNING: No backup will be created!")
        confirm = input("Are you sure? (yes/no): ")
        if confirm.lower() == "yes":
            reset_table()
        else:
            print("Reset cancelled.")
    
    elif choice == "4":
        print("Exiting...")
    
    else:
        print("Invalid choice!")

    print()
    print("=" * 60)
    print("Done!")
    print("=" * 60)
    input("\nPress Enter to exit...")