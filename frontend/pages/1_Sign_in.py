import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"  # Change if your backend runs elsewhere

st.set_page_config(page_title="Sign In - AiThena", page_icon="🔐")

# Check if user is already logged in and redirect to dashboard
if "user_email" in st.session_state and st.session_state.get("logged_in", False):
    st.switch_page("pages/2_Dashboard.py")

st.title("🔐 Sign In to AiThena")
tab1, tab2 = st.tabs(["🔑 Login", "🆕 Sign Up"])

with tab1:
    st.subheader("Welcome back! Please log in:")
    login_email = st.text_input("Email", key="login_email")
    login_password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if not login_email or not login_password:
            st.warning("⚠️ All fields are required.")
        else:
            try:
                response = requests.post(
                    f"{BACKEND_URL}/login",
                    json={"email": login_email, "password": login_password},
                    timeout=10
                )
                data = response.json()
                if response.status_code == 200 and data.get("success"):
                    st.session_state["user_email"] = login_email
                    st.session_state["password"] = login_password
                    st.session_state["logged_in"] = True
                    st.success("✅ Login successful! Redirecting to dashboard...")
                    st.rerun()
                else:
                    st.error(f"❌ {data.get('message', 'Login failed')}")
            except Exception as e:
                st.error(f"❌ Login error: {e}")

with tab2:
    st.subheader("Create a new account:")
    signup_email = st.text_input("Email", key="signup_email")
    signup_password = st.text_input("Password", type="password", key="signup_password")
    signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm")

    if st.button("Sign Up"):
        if signup_password != signup_confirm:
            st.warning("⚠️ Passwords do not match.")
        elif not signup_email or not signup_password:
            st.warning("⚠️ All fields are required.")
        else:
            try:
                response = requests.post(
                    f"{BACKEND_URL}/register",
                    json={"email": signup_email, "password": signup_password},
                    timeout=10
                )
                data = response.json()
                if response.status_code == 200 and data.get("success"):
                    st.success("🎉 Account created! Please log in.")
                else:
                    st.error(f"❌ {data.get('message', 'Registration failed')}")
            except Exception as e:
                st.error(f"❌ Registration error: {e}")
