import streamlit as st
import requests
import json
import os

# --- Page Config ---
st.set_page_config(page_title="PDF Summarizer - AiThena", page_icon="📄")

# --- Auth Check ---
if "user_email" not in st.session_state or not st.session_state.get("logged_in", False):
    st.warning("⚠️ Please sign in to access this page.")
    st.page_link("pages/1_Sign_in.py", label="Go to Sign In", icon="🔐")
    st.stop()

# --- Page Title ---
st.title("📄 PDF Summarizer")
st.markdown("Upload a PDF file to get an AI-powered summary using AiThena's Granite engine.")

# --- File Upload ---
uploaded_file = st.file_uploader("📁 Choose a PDF file", type=['pdf'])

# --- Processing Section ---
if uploaded_file is not None:
    if st.button("🚀 Process PDF"):
        with st.spinner("🔄 Processing PDF..."):
            try:
                # Call backend API for PDF processing
                backend_url = os.getenv("BACKEND_URL", "http://localhost:8000")
                api_endpoint = f"{backend_url}/upload_pdf"
                files = {"file": uploaded_file}
                data = {
                    "email": st.session_state["user_email"],
                    "password": st.session_state.get("password", "")
                }
                
                response = requests.post(api_endpoint, files=files, data=data, timeout=30)
                
                if response.status_code == 200:
                    result = response.json()
                    summaries = result.get("summaries", [])
                    
                    if summaries:
                        st.success(f"✅ PDF processed successfully! Generated {len(summaries)} summaries.")
                        
                        # Display summaries
                        st.markdown("### 📝 Chapter Summaries")
                        
                        for i, summary in enumerate(summaries, 1):
                            with st.expander(f"📖 Chapter {i}: {summary.get('title', 'Untitled')}"):
                                st.markdown(summary.get('summary', 'No summary available'))
                        
                        # Combined summary
                        st.markdown("### 🔗 Combined Summary")
                        combined_text = ""
                        for summary in summaries:
                            combined_text += f"**{summary.get('title', 'Untitled')}:**\n"
                            combined_text += f"{summary.get('summary', '')}\n\n"
                        
                        st.text_area("Complete Summary", combined_text, height=300)
                        
                        # Download option
                        st.download_button(
                            label="📥 Download Summary",
                            data=combined_text,
                            file_name="pdf_summary.txt",
                            mime="text/plain"
                        )
                    else:
                        st.warning("⚠️ No summaries were generated. Please check your PDF content.")
                else:
                    st.error(f"❌ Backend error: {response.status_code}")
                    try:
                        error_detail = response.json()
                        st.error(f"Details: {error_detail}")
                    except:
                        st.error(f"Response: {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend server. Please ensure:")
                st.error("• Backend is running on http://localhost:8000")
                st.error("• No firewall blocking the connection")
                st.error("• Backend service is properly configured")
            except requests.exceptions.Timeout:
                st.error("❌ Request timed out. The server might be overloaded.")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
else:
    st.info("📁 Please upload a PDF file to begin processing.")

# --- Footer ---
st.markdown("---")
st.page_link("pages/2_Dashboard.py", label="🔙 Back to Dashboard", icon="📊")