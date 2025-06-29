import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Quiz Generator - AiThena", page_icon="❓")

# --- Auth Check ---
if "user_email" not in st.session_state:
    st.warning("⚠️ Please sign in to access the Quiz Generator.")
    st.stop()

# --- Page Title ---
st.title("❓ Quiz Generator")
st.markdown("Enter learning material below to generate adaptive quizzes.")

# --- Content Input ---
quiz_input = st.text_area("📄 Paste your content here", height=200)

# --- Generate Quiz Placeholder ---
if st.button("Generate Quiz"):
    if quiz_input.strip():
        st.success("✅ Content received! Generating quiz...")
        st.markdown("### 🧪 Quiz Preview")
        st.write("🔧 Placeholder: Quiz questions and options will be displayed here once implemented.")
    else:
        st.warning("⚠️ Please enter content to generate a quiz.")

# --- Footer ---
st.markdown("---")
st.markdown("🔙 [Back to Dashboard](2_Dashboard.py)")
