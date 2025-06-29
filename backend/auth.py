import bcrypt
import sqlite3

import os
from pathlib import Path
from typing import Optional, Tuple

# Database setup
DB_PATH = Path("data/auth_db/users.db")

def init_db():
    """Initialize the SQLite database with users table"""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if users table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cursor.fetchone()
    
    if not table_exists:
        # Create users table with the existing schema
        cursor.execute('''
            CREATE TABLE users (
                user_email TEXT PRIMARY KEY,
                password_hash TEXT
            )
        ''')
    
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    return password_hash.decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def register_user(email: str, password: str) -> Tuple[bool, str]:
    """Register a new user"""
    try:
        init_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if user already exists
        cursor.execute("SELECT user_email FROM users WHERE user_email = ?", (email,))
        if cursor.fetchone():
            conn.close()
            return False, "User already exists"
        
        # Hash password and store user
        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (user_email, password_hash) VALUES (?, ?)",
            (email, password_hash)
        )
        
        conn.commit()
        conn.close()
        return True, "User registered successfully"
        
    except Exception as e:
        return False, f"Registration failed: {str(e)}"

def authenticate_user(email: str, password: str) -> Tuple[bool, str]:
    """Authenticate a user"""
    try:
        init_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get user by email
        cursor.execute("SELECT password_hash FROM users WHERE user_email = ?", (email,))
        result = cursor.fetchone()
        
        if not result:
            conn.close()
            return False, "User not found"
        
        password_hash = result[0]
        
        # Verify password
        if verify_password(password, password_hash):
            conn.close()
            return True, "Authentication successful"
        else:
            conn.close()
            return False, "Invalid password"
            
    except Exception as e:
        return False, f"Authentication failed: {str(e)}"

def get_user_id(email: str) -> Optional[str]:
    """Get user email (used as ID in this schema)"""
    try:
        init_db()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_email FROM users WHERE user_email = ?", (email,))
        result = cursor.fetchone()
        
        conn.close()
        return result[0] if result else None
        
    except Exception:
        return None

def store_user_result(user_email: str, result: dict) -> bool:
    """Store user quiz result"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create results table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                result TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_email) REFERENCES users (user_email)
            )
        ''')
        
        cursor.execute(
            "INSERT INTO user_results (user_email, result) VALUES (?, ?)",
            (user_email, str(result))
        )
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Failed to store user result: {e}")
        return False

def store_user_feedback(user_email: str, feedback: str) -> bool:
    """Store user feedback"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Create feedback table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_email TEXT NOT NULL,
                feedback TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_email) REFERENCES users (user_email)
            )
        ''')
        
        cursor.execute(
            "INSERT INTO user_feedback (user_email, feedback) VALUES (?, ?)",
            (user_email, feedback)
        )
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Failed to store user feedback: {e}")
        return False 
