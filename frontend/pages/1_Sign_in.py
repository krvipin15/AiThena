import streamlit as st
import sys
import os

# Add backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from backend.auth import init_db, register_user, authenticate_user

# Initialize the DB
init_db()

st.set_page_config(page_title="Sign In - AiThena", page_icon="🔐")

# Check if user is already logged in and redirect to dashboard
if "user_email" in st.session_state and st.session_state.get("logged_in", False):
    st.switch_page("pages/2_Dashboard")

# --- Page Title ---
st.title("🔐 Sign In to AiThena")

# --- Tabs for Login and Sign Up ---
tab1, tab2 = st.tabs(["🔑 Login", "🆕 Sign Up"])

# --- Login Tab ---
with tab1:
    st.subheader("Welcome back! Please log in:")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        success, message = authenticate_user(login_email, login_password)
        if success:
            st.session_state["user_email"] = login_email
            st.session_state["password"] = login_password
            st.session_state["logged_in"] = True
            st.success("✅ Login successful! Redirecting to dashboard...")
            st.rerun()
        else:
            st.error(f"❌ {message}")

# --- Sign Up Tab ---
with tab2:
    st.subheader("Create a new account:")
    signup_email = st.text_input("Email", key="signup_email")
    signup_password = st.text_input("Password", type="password", key="signup_password")
    signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")

    if st.button("Sign Up"):
        if signup_password != signup_confirm:
            st.warning("⚠️ Passwords do not match.")
        elif signup_email == "" or signup_password == "":
            st.warning("⚠️ All fields are required.")
        else:
            success, message = register_user(signup_email, signup_password)
            if success:
                st.success("🎉 Account created successfully! Please log in.")
            else:
                st.error(f"❌ {message}")
