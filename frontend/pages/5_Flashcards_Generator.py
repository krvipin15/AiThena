import streamlit as st
import requests
import json

# --- Page Config ---
st.set_page_config(page_title="Flashcards Generator - AiThena", page_icon="📚")

# --- Auth Check ---
if "user_email" not in st.session_state:
    st.warning("⚠️ Please sign in to access the Flashcards Generator.")
    st.stop()

# --- Page Title ---
st.title("📚 Flashcards Generator")
st.markdown("Generate interactive flashcards from any text content using AiThena's AI engine.")

# --- Text Input ---
text_input = st.text_area("📝 Enter your text content", height=200, 
                         placeholder="Paste your study material, lecture notes, or any text content here...")

# --- Processing Section ---
if text_input:
    if st.button("🚀 Generate Flashcards"):
        with st.spinner("🔄 Generating flashcards..."):
            try:
                # Call backend API for flashcard generation
                backend_url = "http://localhost:8000/generate_flashcards"
                data = {
                    "text": text_input,
                    "email": st.session_state["user_email"],
                    "password": st.session_state.get("password", "")
                }
                
                response = requests.post(backend_url, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    flashcards = result.get("flashcards", [])
                    
                    if flashcards:
                        st.success(f"✅ Generated {len(flashcards)} flashcards!")
                        
                        # Display flashcards
                        st.markdown("### 🎯 Your Flashcards")
                        
                        for i, flashcard in enumerate(flashcards, 1):
                            with st.expander(f"📖 Flashcard {i}"):
                                st.markdown(f"**Question:** {flashcard.get('question', '')}")
                                st.markdown(f"**Answer:** {flashcard.get('answer', '')}")
                        
                        # Download option
                        flashcard_text = ""
                        for i, flashcard in enumerate(flashcards, 1):
                            flashcard_text += f"Flashcard {i}:\n"
                            flashcard_text += f"Q: {flashcard.get('question', '')}\n"
                            flashcard_text += f"A: {flashcard.get('answer', '')}\n\n"
                        
                        st.download_button(
                            label="📥 Download Flashcards",
                            data=flashcard_text,
                            file_name="flashcards.txt",
                            mime="text/plain"
                        )
                    else:
                        st.warning("⚠️ No flashcards were generated. Please try with different content.")
                else:
                    st.error(f"❌ Backend error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend server. Please make sure the backend is running on http://localhost:8000")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
else:
    st.info("📝 Please enter some text content to generate flashcards.")

# --- Footer ---
st.markdown("---")
st.page_link("pages/2_Dashboard.py", label="🔙 Back to Dashboard", icon="📊")
