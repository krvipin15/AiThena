import bcrypt
import sqlite3
import streamlit as st
from pathlib import Path

data_dir = Path("data")
db_path = data_dir / "auth_db" / "users.db"

def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_email TEXT PRIMARY KEY,
            password_hash TEXT
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

def main():
    st.title("🔐 Login / Signup Demo")
    init_db()

    menu = ["Login", "Signup"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type='password')

        if st.button("Login"):
            if authenticate_user(username, password):
                st.success(f"Welcome, {username}!")
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                show_app()
            else:
                st.error("Invalid username or password")

    elif choice == "Signup":
        st.subheader("Create New Account")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type='password')

        if st.button("Signup"):
            if add_user(new_user, new_pass):
                st.success("Account created successfully! Go to Login.")
            else:
                st.warning("Username already exists. Try a different one.")

def show_app():
    st.write("🎉 You're logged in!")
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.experimental_rerun()

# Entry point
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if st.session_state['logged_in']:
    show_app()
else:
    main()
