import streamlit as st
import requests
import json

# --- Page Config ---
st.set_page_config(page_title="Quiz Generator - AiThena", page_icon="🧠")

# --- Auth Check ---
if "user_email" not in st.session_state:
    st.warning("⚠️ Please sign in to access the Quiz Generator.")
    st.stop()

# --- Page Title ---
st.title("🧠 Quiz Generator")
st.markdown("Generate multiple choice questions from any text content using AiThena's AI engine.")

# --- Text Input ---
text_input = st.text_area("📝 Enter your text content", height=200, 
                         placeholder="Paste your study material, lecture notes, or any text content here...")

# --- Processing Section ---
if text_input:
    if st.button("🚀 Generate Quiz"):
        with st.spinner("🔄 Generating quiz questions..."):
            try:
                # Call backend API for MCQ generation
                backend_url = "http://localhost:8000/generate_mcq"
                data = {
                    "text": text_input,
                    "email": st.session_state["user_email"],
                    "password": st.session_state.get("password", "")
                }
                
                response = requests.post(backend_url, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    mcqs = result.get("mcqs", [])
                    
                    if mcqs:
                        st.success(f"✅ Generated {len(mcqs)} quiz questions!")
                        
                        # Display quiz questions
                        st.markdown("### 🎯 Your Quiz")
                        
                        for i, mcq in enumerate(mcqs, 1):
                            with st.expander(f"❓ Question {i}"):
                                st.markdown(f"**{mcq.get('question', '')}**")
                                
                                # Display choices
                                choices = mcq.get('choices', [])
                                for j, choice in enumerate(choices):
                                    st.write(f"{choice}")
                                
                                # Show answer
                                st.markdown(f"**Correct Answer:** {mcq.get('answer', '')}")
                        
                        # Interactive quiz mode
                        st.markdown("### 🎮 Interactive Quiz Mode")
                        st.info("Take the quiz interactively:")
                        
                        for i, mcq in enumerate(mcqs, 1):
                            st.markdown(f"**{i}. {mcq.get('question', '')}**")
                            choices = mcq.get('choices', [])
                            user_answer = st.radio(
                                f"Select your answer for question {i}:",
                                [choice.split(") ")[1] if ") " in choice else choice for choice in choices],
                                key=f"q{i}"
                            )
                            
                            if st.button(f"Check Answer {i}", key=f"check{i}"):
                                correct_answer = mcq.get('answer', '')
                                if user_answer == correct_answer:
                                    st.success("✅ Correct!")
                                else:
                                    st.error(f"❌ Incorrect. The correct answer is: {correct_answer}")
                        
                        # Download option
                        quiz_text = ""
                        for i, mcq in enumerate(mcqs, 1):
                            quiz_text += f"Question {i}:\n"
                            quiz_text += f"{mcq.get('question', '')}\n"
                            choices = mcq.get('choices', [])
                            for choice in choices:
                                quiz_text += f"{choice}\n"
                            quiz_text += f"Answer: {mcq.get('answer', '')}\n\n"
                        
                        st.download_button(
                            label="📥 Download Quiz",
                            data=quiz_text,
                            file_name="quiz.txt",
                            mime="text/plain"
                        )
                    else:
                        st.warning("⚠️ No quiz questions were generated. Please try with different content.")
                else:
                    st.error(f"❌ Backend error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend server. Please make sure the backend is running on http://localhost:8000")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
else:
    st.info("📝 Please enter some text content to generate quiz questions.")

# --- Footer ---
st.markdown("---")
st.markdown("🔙 [Back to Dashboard](pages/2_Dashboard)")
