import bcrypt
import sqlite3
from pathlib import Path

# Setup paths
data_dir = Path("data") / "auth_db"
data_dir.mkdir(parents=True, exist_ok=True)
db_path = data_dir / "users.db"

def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_email TEXT PRIMARY KEY,
            password_hash BLOB
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def add_user(email, password):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    hashed = hash_password(password)
    try:
        c.execute('INSERT INTO users (user_email, password_hash) VALUES (?, ?)', (email, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def authenticate_user(email, password):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT password_hash FROM users WHERE user_email = ?', (email,))
    result = c.fetchone()
    conn.close()
    if result:
        return check_password(password, result[0])
    return False
