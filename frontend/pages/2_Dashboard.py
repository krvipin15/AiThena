import streamlit as st

# Redirect if user is not logged in
if "user_email" not in st.session_state or not st.session_state.get("logged_in", False):
    st.warning("⚠️ Please sign in to access the dashboard.")
    st.stop()

st.set_page_config(page_title="Dashboard - AiThena", page_icon="📊")

# --- Welcome Header ---
st.markdown(f"## 👋 Welcome, {st.session_state['user_email']}")
st.markdown("### 📚 Your Personalized Learning Dashboard")

# --- Dashboard Navigation Cards ---
st.markdown("---")
cols = st.columns(3)

with cols[0]:
    st.markdown("#### 📄 PDF Summarizer")
    st.page_link("pages/3_PDF_Summarizer", label="Open Tool", icon="🔍")

with cols[1]:
    st.markdown("#### 🎥 YouTube Summarizer")
    st.page_link("pages/4_YouTube_Summarizer", label="Open Tool", icon="🎬")

with cols[2]:
    st.markdown("#### 🧠 Flashcards Generator")
    st.page_link("pages/5_Flashcards_Generator", label="Open Tool", icon="📝")

cols = st.columns(2)

with cols[0]:
    st.markdown("#### ❓ Quiz Generator")
    st.page_link("pages/6_Quiz_Generator", label="Open Tool", icon="🧪")

with cols[1]:
    st.markdown("#### 📈 Progress Tracker")
    st.page_link("pages/7_Progress_Tracker", label="Open Tool", icon="📊")

# --- Footer ---
st.markdown("---")
if st.button("🔓 Log Out"):
    st.session_state.clear()
    st.success("You have been logged out.")
    st.rerun()
