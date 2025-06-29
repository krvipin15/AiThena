import base64
from PIL import Image
from io import BytesIO
import streamlit as st
from pathlib import Path
import time
from streamlit_lottie import st_lottie
import requests


# Initialize image directory path
img_path = Path("frontend") / "assets" / "logo.png"

# Load logo with fallback
try:
    logo = Image.open(img_path)
except FileNotFoundError:
    st.warning("⚠️ Logo not found. Using fallback image.")
    logo = Image.new("RGB", (100, 100), color="gray")  # Placeholder image

# Page config
st.set_page_config(page_title="AiThena", page_icon=logo, layout="wide")

# Utility: Convert logo image to base64
def logo_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Hide sidebar and toggle
hide_sidebar_style = """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# Custom CSS including mobile responsiveness and fade-in animation
st.markdown("""
    <style>
    .main {
        background-color: white;
        font-family: 'Segoe UI', sans-serif;
    }

    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 3rem;
        background-color: #ffffff;
        border-bottom: 3px solid #e2e8f0;
        position: fixed;
        width: 90%;
        top:0;
        z-index: 100;
    }

    .logo-title {
        display: flex;
        align-items: center;
    }

    .logo-title img {
        height: 45px;
        margin-right: 0.8rem;
    }

    .logo-title span {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2563eb;
    }

    .sign-in-btn {
        background-color: #ffffff;
        border: 1px solid #cbd5e1;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-size: 0.9rem;
        cursor: pointer;
    }

    .hero .main-content {
        text-align: center;
        padding: 8rem 6rem 3rem 2rem;
        animation: fadeIn 1.5 s ease-in-out;
    }

    .hero h1 {
        font-size: 2.8rem;
        font-weight: bold;
        color: #0f172a;
        margin-bottom: 1rem;
    }

    .hero p {
        font-size: 1.1rem;
        color: #475569;
    }

    .cta-button {
        margin: 2rem 0;
        background-color: #2563eb;
        color: white;
        padding: 1rem 1.8rem;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1rem;
        cursor: pointer;
    }

    .cta-button-link {
        display: inline-block;
        background-color: #2563eb;
        color: white;
        padding: 1rem 1.8rem;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        font-size: 1rem;
        cursor: pointer;
        text-decoration: none;
    }

    .course-tags {
        display: flex;
        text-align: center;
        flex-direction: column;
        justify-content: center;
        margin-top: 0.5rem;
        padding: 0.2rem 6rem 5rem 2rem;
    }

    .course-tags strong {
        margin-bottom: 0.8rem;
    }

    .tags-container {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        justify-content: center;
    }

    .tag {
        background-color: #e0ecff;
        padding: 0.4rem 1rem;
        margin: 0.4rem;
        border-radius: 6px;
        font-family: monospace;
        display: inline-block;
    }

    .footer {
        text-align: center;
        font-size: 0.9rem;
        color: #1e293b;
        margin-top: 7rem;
        padding-bottom: 2rem;
        border-top: 2px solid #cbd5e1;
        padding-top: 1rem;
        position: fixed;
        width: 90%;
        bottom: 0;
        background: white;
    }
     
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(20px);}
        to {opacity: 1; transform: translateY(0);}
    }

    /* Mobile responsiveness */
    @media screen and (max-width: 768px) {
        .nav-bar {
            flex-direction: column;
            align-items: flex-start;
            padding: 1rem;
            width: 100%;
        }

        .logo-title {
            margin-bottom: 1rem;
        }

        .footer {
            font-size: 0.75rem;
            width: 100%;
            text-align: left;
            padding: 1rem;
        }

        .hero, .main-content {
            padding: 6rem 1.5rem 2rem 1rem;
        }

        .hero h1 {
            font-size: 1.8rem;
        }

        .hero p {
            font-size: 1rem;
        }

        .cta-button, .cta-button-link {
            font-size: 0.9rem;
            padding: 0.7rem 1.4rem;
        }

        .tags-container {
            justify-content: flex-start;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Navigation bar (always  vissible)
st.markdown(f"""
    <div class="nav-bar">
        <div class="logo-title">
            <img src="data:image/png;base64,{logo_to_base64(logo)}" alt="Logo"/>
            <span>AiThena</span>
        </div>
        <form action="/login" method="get">
            <button class="sign-in-btn" type="submit">Sign In</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# Animated Intro Section

# Container placeholders
intro_container = st.container()
main_container = st.container()

with intro_container:
    animated_text_placeholder = st.empty()
    # Load Lottie animation JSON
    def load_lottieurl(url):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    lottie_url = "https://assets2.lottiefiles.com/packages/lf20_touohxv0.json"
    lottie_json = load_lottieurl(lottie_url)

    if lottie_json:
        st_lottie(lottie_json, height=250, key="intro_animation")
    else:
        st.write("🎬 Loading animation...")

    messages = [
        "Welcome to AiThena...",
        "Personalized AI-Powered Learning",
        "Adaptive quizzes and feedback",
        "Your journey starts here!"
    ]

    for msg in messages:
        animated_text_placeholder.markdown(f"<h2 style='color:#2563eb'>{msg}</h2>", unsafe_allow_html=True)
        time.sleep(1.5)

# 
# Hide intro, show main content after animation
intro_container.empty()

with main_container:
    st.markdown("""
    <div class="hero">
        <h1>AI-Powered Learning Revolution<br>Transform Any Content Into Your Personal Curriculum</h1>
        <p>At AiThena, we believe that education should be tailored to your unique needs and learning style. <br>Our adaptive AI tutor uses advanced Granite models to provide personalized explanations, quizzes, and feedback, making learning more engaging and effective.</p>
        <a href="/Login" class="cta-button-link">Begin Adaptive Learning</a>
    </div>
""", unsafe_allow_html=True)

# Course Tags
st.markdown("""
    <div class="course-tags">
        <strong>Popular courses:</strong>
        <div class="tags-container">
            <span class="tag">Essential ML and AI Concepts</span>
            <span class="tag">German for Beginner</span>
            <span class="tag">N8N Automation Agents</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        © 2025 AiThena | About Us | Contact Us | Privacy Policy | Terms & Conditions
    </div>
""", unsafe_allow_html=True)
