import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Flashcards Generator - AiThena", page_icon="🧠")

# --- Auth Check ---
if "user_email" not in st.session_state:
    st.warning("⚠️ Please sign in to access the Flashcards Generator.")
    st.stop()

# --- Page Title ---
st.title("🧠 Flashcards Generator")
st.markdown("Turn your notes, summaries, or transcripts into interactive flashcards.")

# --- Content Input ---
content_input = st.text_area("📄 Paste your learning content here", height=200)

# --- Generate Flashcards Placeholder ---
if st.button("Generate Flashcards"):
    if content_input.strip():
        st.success("✅ Content received! Flashcards will be generated here.")
        st.markdown("### 🃏 Flashcards Output")
        st.write("🔧 Placeholder: Flashcards will appear here once implemented.")
    else:
        st.warning("⚠️ Please enter some content to generate flashcards.")

# --- Footer ---
st.markdown("---")
st.markdown("🔙 [Back to Dashboard](2_Dashboard.py)")
