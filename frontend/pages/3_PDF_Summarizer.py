import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="PDF Summarizer - AiThena", page_icon="📄")

# --- Auth Check ---
if "user_email" not in st.session_state:
    st.warning("⚠️ Please sign in to access the PDF Summarizer.")
    st.stop()

# --- Page Title ---
st.title("📄 PDF Summarizer")
st.markdown("Upload your PDF files to generate a personalized summary powered by AiThena's AI.")

# --- File Uploader ---
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

# --- Placeholder for Summary Output ---
if uploaded_file:
    st.info("✅ File uploaded successfully!")
    st.markdown("### ✨ Summary Output")
    st.write("🔧 This is a placeholder for the generated summary.")
    st.write("➡️ You'll see the AI summary here once the backend is integrated.")
else:
    st.info("📂 Please upload a PDF file to get started.")

# --- Footer ---
st.markdown("---")
st.markdown("🔙 [Back to Dashboard](2_Dashboard.py)")
