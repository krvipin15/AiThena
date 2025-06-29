import streamlit as st
import requests
import json

# --- Page Config ---
st.set_page_config(page_title="Quiz Generator - AiThena", page_icon="🧠")

# --- Auth Check ---
if "user_email" not in st.session_state or not st.session_state.get("logged_in", False):
    st.warning("⚠️ Please sign in to access the Quiz Generator.")
    st.page_link("1_Sign_in", label="Go to Sign In", icon="🔐")
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
                        
                        # Store MCQs in session state for interactive mode
                        st.session_state["current_mcqs"] = mcqs
                        st.session_state["quiz_generated"] = True
                        
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
                                correct_answer = mcq.get('answer', '')
                                st.markdown(f"**Correct Answer:** {correct_answer}")
                        
                        # Interactive quiz mode
                        st.markdown("### 🎮 Interactive Quiz Mode")
                        st.info("Take the quiz interactively and get instant feedback!")
                        
                        # Initialize session state for quiz tracking
                        if "quiz_answers" not in st.session_state:
                            st.session_state["quiz_answers"] = {}
                        if "quiz_results" not in st.session_state:
                            st.session_state["quiz_results"] = {}
                        if "quiz_submitted" not in st.session_state:
                            st.session_state["quiz_submitted"] = False
                        
                        total_questions = len(mcqs)
                        
                        # Create choice mapping for all questions (outside form)
                        all_choice_mappings = {}
                        for i, mcq in enumerate(mcqs, 1):
                            choices = mcq.get('choices', [])
                            choice_mapping = {}
                            
                            for choice in choices:
                                if choice.startswith('A)') or choice.startswith('B)') or choice.startswith('C)') or choice.startswith('D)'):
                                    # Extract the letter and text
                                    parts = choice.split(') ', 1)
                                    if len(parts) == 2:
                                        letter = parts[0]
                                        text = parts[1]
                                        choice_mapping[text] = letter
                            
                            all_choice_mappings[i] = choice_mapping
                        
                        # Display questions and collect answers
                        for i, mcq in enumerate(mcqs, 1):
                            st.markdown(f"**{i}. {mcq.get('question', '')}**")
                            choices = mcq.get('choices', [])
                            
                            # Create choice options for radio button
                            choice_options = []
                            
                            for choice in choices:
                                if choice.startswith('A)') or choice.startswith('B)') or choice.startswith('C)') or choice.startswith('D)'):
                                    # Extract the letter and text
                                    parts = choice.split(') ', 1)
                                    if len(parts) == 2:
                                        text = parts[1]
                                        choice_options.append(text)
                                    else:
                                        choice_options.append(choice)
                                else:
                                    choice_options.append(choice)
                            
                            # User selects answer
                            user_answer_text = st.radio(
                                f"Select your answer for question {i}:",
                                choice_options,
                                key=f"q{i}"
                            )
                            
                            # Store user's answer
                            st.session_state["quiz_answers"][i] = user_answer_text
                        
                        # Submit button (outside form)
                        if st.button("📝 Submit Quiz"):
                            st.session_state["quiz_submitted"] = True
                            st.rerun()
                        
                        # Show results only after submission
                        if st.session_state.get("quiz_submitted", False):
                            st.markdown("### 📊 Quiz Results")
                            
                            correct_answers = 0
                            
                            for i, mcq in enumerate(mcqs, 1):
                                st.markdown(f"**{i}. {mcq.get('question', '')}**")
                                
                                # Get user's answer
                                user_answer_text = st.session_state["quiz_answers"].get(i, "")
                                correct_answer_letter = mcq.get('answer', '')
                                choice_mapping = all_choice_mappings.get(i, {})
                                user_answer_letter = choice_mapping.get(user_answer_text, '')
                                
                                is_correct = user_answer_letter == correct_answer_letter
                                st.session_state["quiz_results"][i] = is_correct
                                
                                if is_correct:
                                    correct_answers += 1
                                    st.success(f"✅ Your answer: {user_answer_text} - Correct!")
                                else:
                                    st.error(f"❌ Your answer: {user_answer_text} - Incorrect. The correct answer is: {correct_answer_letter}")
                            
                            # Calculate and display score
                            score_percentage = (correct_answers / total_questions) * 100
                            st.markdown("---")
                            st.markdown(f"**Final Score: {correct_answers}/{total_questions} ({score_percentage:.1f}%)**")
                            
                            if score_percentage >= 80:
                                st.success("🎉 Excellent! Great job!")
                            elif score_percentage >= 60:
                                st.info("👍 Good work! Keep studying!")
                            else:
                                st.warning("📚 Keep practicing! Review the material and try again.")
                            
                            # Generate feedback
                            if st.button("💡 Get Personalized Feedback"):
                                with st.spinner("🔄 Generating feedback..."):
                                    try:
                                        # Prepare quiz results for feedback
                                        quiz_summary = f"Score: {correct_answers}/{total_questions} ({score_percentage:.1f}%). "
                                        
                                        # Build questions summary separately to avoid f-string issues
                                        questions_summary = []
                                        for i in range(1, total_questions + 1):
                                            result = "Correct" if st.session_state["quiz_results"].get(i, False) else "Incorrect"
                                            questions_summary.append(f"Q{i}: {result}")
                                        
                                        quiz_summary += f"Questions answered: {', '.join(questions_summary)}"
                                        
                                        feedback_url = "http://localhost:8000/feedback"
                                        feedback_data = {
                                            "email": st.session_state["user_email"],
                                            "password": st.session_state.get("password", ""),
                                            "quiz_results": quiz_summary
                                        }
                                        
                                        feedback_response = requests.post(feedback_url, data=feedback_data)
                                        
                                        if feedback_response.status_code == 200:
                                            feedback_result = feedback_response.json()
                                            st.markdown("### 💡 Personalized Feedback")
                                            st.write(feedback_result.get("feedback", "No feedback available."))
                                        else:
                                            st.error("❌ Error generating feedback")
                                            
                                    except Exception as e:
                                        st.error(f"❌ Error: {str(e)}")
                        
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
st.page_link("pages/2_Dashboard.py", label="🔙 Back to Dashboard", icon="📊")
