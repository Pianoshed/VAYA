"""
Run this script ONCE to add the missing 'page' and 'user_agent' columns
to the existing page_visit table.

Usage:
    python migrate_page_visit.py
"""

import sqlite3
import os

# Search for ALL .db files starting from the script's directory
search_dir = os.path.dirname(os.path.abspath(__file__))

print(f"Searching for .db files in: {search_dir}")
db_files = []
for root, dirs, files in os.walk(search_dir):
    for f in files:
        if f.endswith('.db'):
            db_files.append(os.path.join(root, f))

if not db_files:
    print(" No .db files found. Make sure you've run the Flask app at least once first.")
    exit(1)

print("Found database files:")
for i, f in enumerate(db_files):
    print(f"  [{i}] {f}")

# Prefer default.db, otherwise use the first found
target_db = next((f for f in db_files if os.path.basename(f) == 'default.db'), db_files[0])
print(f"\nUsing: {target_db}")

conn = sqlite3.connect(target_db)
cursor = conn.cursor()

# Show all tables in this database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print(f"Tables found: {tables}")

if 'page_visit' not in tables:
    print("\n  'page_visit' table does not exist — creating it fresh with all columns.")
    cursor.execute("""
        CREATE TABLE page_visit (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address VARCHAR(100),
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            location VARCHAR(255),
            page VARCHAR(100) DEFAULT '/',
            user_agent VARCHAR(255)
        )
    """)
    print(" Created table: page_visit")
else:
    cursor.execute("PRAGMA table_info(page_visit)")
    existing_cols = [row[1] for row in cursor.fetchall()]
    print(f"Existing columns in page_visit: {existing_cols}")

    if 'page' not in existing_cols:
        cursor.execute("ALTER TABLE page_visit ADD COLUMN page VARCHAR(100) DEFAULT '/'")
        print(" Added column: page")
    else:
        print("⏭  Column 'page' already exists, skipping.")

    if 'user_agent' not in existing_cols:
        cursor.execute("ALTER TABLE page_visit ADD COLUMN user_agent VARCHAR(255)")
        print(" Added column: user_agent")
    else:
        print("⏭  Column 'user_agent' already exists, skipping.")

conn.commit()
conn.close()

print("\n Done. Restart your Flask app.")