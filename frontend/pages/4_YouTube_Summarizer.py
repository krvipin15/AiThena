import streamlit as st
import requests
import json

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

# --- Processing Section ---
if youtube_url:
    if st.button("🚀 Process Video"):
        with st.spinner("🔄 Processing YouTube video..."):
            try:
                # Call backend API for YouTube processing
                backend_url = "http://localhost:8000/process_youtube"
                data = {
                    "youtube_url": youtube_url,
                    "email": st.session_state["user_email"],
                    "password": st.session_state.get("password", "")  # You might need to store this
                }
                
                response = requests.post(backend_url, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("success"):
                        st.success("✅ Video processed successfully!")
                        
                        # Display transcript
                        with st.expander("📝 View Transcript"):
                            st.text_area("Transcript", result.get("transcript", ""), height=200)
                        
                        # Display summary
                        st.markdown("### ✨ AI-Generated Summary")
                        st.write(result.get("summary", "No summary available"))
                        
                        # Display video info
                        video_info = result.get("video_info", {})
                        if video_info:
                            st.markdown("### 📊 Video Information")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Duration", video_info.get("duration", "Unknown"))
                            with col2:
                                st.metric("Transcript Length", video_info.get("transcript_length", 0))
                            with col3:
                                st.metric("Available", "✅" if video_info.get("transcript_available") else "❌")
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Unknown error')}")
                else:
                    st.error(f"❌ Backend error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend server. Please make sure the backend is running on http://localhost:8000")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
else:
    st.info("🎬 Please enter a valid YouTube link to begin.")

# --- Footer ---
st.markdown("---")
st.markdown("🔙 [Back to Dashboard](pages/2_Dashboard)")
