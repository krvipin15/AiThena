import streamlit as st

if "user_email" not in st.session_state or not st.session_state.get("logged_in", False):
    st.warning("⚠️ Please sign in to access the dashboard.")
    st.page_link("pages/1_Sign_in.py", label="Go to Sign In", icon="🔐")
    st.stop()

st.set_page_config(page_title="Dashboard - AiThena", page_icon="📊")

st.markdown(f"## 👋 Welcome, {st.session_state['user_email']}")
st.markdown("### 📚 Your Personalized Learning Dashboard")

st.markdown("---")
cols = st.columns(3)

with cols[0]:
    st.markdown("#### 📄 PDF Summarizer")
    st.page_link("pages/3_PDF_Summarizer.py", label="Open Tool", icon="🔍")

with cols[1]:
    st.markdown("#### 🎥 YouTube Summarizer")
    st.page_link("pages/4_YouTube_Summarizer.py", label="Open Tool", icon="🎬")

with cols[2]:
    st.markdown("#### 🧠 Flashcards Generator")
    st.page_link("pages/5_Flashcards_Generator.py", label="Open Tool", icon="📝")

cols = st.columns(2)

with cols[0]:
    st.markdown("#### ❓ Quiz Generator")
    st.page_link("pages/6_Quiz_Generator.py", label="Open Tool", icon="🧪")

with cols[1]:
    st.markdown("#### 📈 Progress Tracker")
    st.page_link("pages/7_Progress_Tracker.py", label="Open Tool", icon="📊")

st.markdown("---")
if st.button("🔓 Log Out"):
    st.session_state.clear()
    st.success("You have been logged out.")
    st.switch_page("pages/1_Sign_in.py")