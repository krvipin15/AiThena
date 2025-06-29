import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="YouTube Summarizer - AiThena", page_icon="🎥")

# --- Auth Check ---
if "user_email" not in st.session_state:
    st.warning("⚠️ Please sign in to access the YouTube Summarizer.")
    st.stop()

# --- Page Title ---
st.title("🎥 YouTube Summarizer")
st.markdown("Paste a YouTube video link to get a smart summary using AiThena's AI engine.")

# --- YouTube Link Input ---
youtube_url = st.text_input("🔗 Enter YouTube video URL")

# --- Placeholder for Summary Output ---
if youtube_url:
    st.info("✅ URL received. Processing will happen here.")
    st.markdown("### ✨ Summary Output")
    st.write("🔧 This is a placeholder for the AI-generated summary from the transcript.")
    st.write("➡️ The summary will appear here once the backend is implemented.")
else:
    st.info("🎬 Please enter a valid YouTube link to begin.")

# --- Footer ---
st.markdown("---")
st.markdown("🔙 [Back to Dashboard](2_Dashboard.py)")
