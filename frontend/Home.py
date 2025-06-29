from PIL import Image
import streamlit as st
from pathlib import Path

# Initialize image directory path
img_path = Path("frontend/assets") / "logo.png"

# Load logo
logo = Image.open(img_path)

# Set page config
st.set_page_config(page_title="AiThena - Personalized AI Tutor", page_icon=logo, layout="centered")

# --- Header ---
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>AiThena</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>AI-Powered Learning Revolution</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Transform Any Content Into Your Personal Curriculum</p>", unsafe_allow_html=True)

# --- Subheading Text ---
st.markdown("""
<div style="text-align: center; margin-top: 30px;">
    <p style="font-size:16px;">
        At <strong>AiThena</strong>, we believe that education should be tailored to your unique needs and learning style. <br>
        Our adaptive AI tutor uses advanced Granite models to provide personalized explanations, quizzes, and feedback, <br>
        making learning more engaging and effective.
    </p>
</div>
""", unsafe_allow_html=True)

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style="text-align: center; font-size: 14px;">
    © 2025 AiThena |
    <a href='#'>About Us</a> |
    <a href='#'>Contact Us</a> |
    <a href='#'>Privacy Policy</a> |
    <a href='#'>Terms & Conditions</a>
</div>
""", unsafe_allow_html=True)
