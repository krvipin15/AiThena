import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="Progress Tracker - AiThena", page_icon="📈")

# --- Auth Check ---
if "user_email" not in st.session_state:
    st.warning("⚠️ Please sign in to access the Progress Tracker.")
    st.stop()

# --- Page Title ---
st.title("📈 Progress Tracker")
st.markdown("Track your learning journey, completed quizzes, and growth over time.")

# --- Placeholder Progress Metrics ---
st.markdown("### 🧩 Learning Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Modules Completed", "5", "↑ 2 this week")
col2.metric("Quizzes Taken", "12", "↑ 4 this week")
col3.metric("Accuracy", "87%", "↑ 5%")

# --- Placeholder for Progress Graphs ---
st.markdown("### 📊 Progress Over Time")
st.info("🔧 Placeholder: Progress charts will be displayed here once data is available.")

# You can later add matplotlib, plotly, or Recharts charts here.

# --- Footer ---
st.markdown("---")
st.markdown("🔙 [Back to Dashboard](2_Dashboard.py)")
