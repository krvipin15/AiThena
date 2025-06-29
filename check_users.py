import sqlite3
from pathlib import Path

DB_PATH = Path("data/auth_db/users.db")

if DB_PATH.exists():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_email FROM users")
    users = cursor.fetchall()
    
    print(f"📊 Found {len(users)} registered users:")
    for user in users:
        print(f"  📧 {user[0]}")
    
    conn.close()
else:
    print("❌ No database found yet. Register a user first!")