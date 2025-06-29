import streamlit as st
import requests
import json

# --- Page Config ---
st.set_page_config(page_title="PDF Summarizer - AiThena", page_icon="📄")

# --- Auth Check ---
if "user_email" not in st.session_state:
    st.warning("⚠️ Please sign in to access the PDF Summarizer.")
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
                backend_url = "http://localhost:8000/upload_pdf"
                files = {"file": uploaded_file}
                data = {
                    "email": st.session_state["user_email"],
                    "password": st.session_state.get("password", "")
                }
                
                response = requests.post(backend_url, files=files, data=data)
                
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
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend server. Please make sure the backend is running on http://localhost:8000")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
else:
    st.info("📁 Please upload a PDF file to begin processing.")

# --- Footer ---
st.markdown("---")
st.markdown("🔙 [Back to Dashboard](pages/2_Dashboard)")
