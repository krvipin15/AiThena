import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Granite API Configuration - Use environment variables for security
GRANITE_API_KEY = os.getenv("GRANITE_API_KEY")
GRANITE_API_URL = os.getenv("GRANITE_API_URL", "https://us-south.ml.cloud.ibm.com")
PROJECT_ID = os.getenv("PROJECT_ID")

# Validate required environment variables
if not GRANITE_API_KEY:
    raise ValueError("GRANITE_API_KEY environment variable is required. Please set it in your .env file.")

if not PROJECT_ID:
    raise ValueError("PROJECT_ID environment variable is required. Please set it in your .env file.")

# Function to get IAM access token from API key
def get_iam_token(api_key):
    url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key,
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def call_granite_api(prompt: str, model: str = "ibm/granite-3-3-8b-instruct", max_tokens: int = 1000) -> str:
    """Make a call to the Granite API using the correct IBM watsonx.ai format"""
    try:
        # Get IAM access token
        iam_token = get_iam_token(GRANITE_API_KEY)
        headers = {
            "Authorization": f"Bearer {iam_token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        payload = {
            "model_id": model,
            "input": prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": 0.3,
                "top_p": 0.9,
                "decoding_method": "greedy",
                "repetition_penalty": 1.1
            },
            "project_id": PROJECT_ID
        }
        
        api_endpoint = f"{GRANITE_API_URL}/ml/v1-beta/generation/text?version=2024-05-29"
        
        print(f"Calling Granite API...")
        print(f"Model: {model}")
        
        response = requests.post(api_endpoint, headers=headers, json=payload)
        print(f"Response status: {response.status_code}")
        
        response.raise_for_status()
        result = response.json()
        
        # Extract the generated text from the response
        if "results" in result and result["results"]:
            generated_text = result["results"][0].get("generated_text", "").strip()
            return generated_text
        else:
            print(f"No results in response")
            return str(result)
            
    except Exception as e:
        print(f"Error calling Granite API: {e}")
        return f"[Error: {str(e)}]"

def generate_youtube_summary(transcript: str, video_title: str = "") -> str:
    """Generate a comprehensive summary specifically for YouTube videos"""
    prompt = f"""Create a detailed and engaging summary of this YouTube video:

Video Title: {video_title if video_title else "Computer Basics Course"}

Transcript:
{transcript[:4000]}

Please create a comprehensive summary that includes:

**Main Topic & Overview**
- What is this video about?
- Who is the target audience?

**Key Points Covered**
- List the main concepts and topics discussed
- Include specific examples or demonstrations mentioned

**Important Takeaways**
- What should viewers remember from this video?
- What practical knowledge or skills are gained?

**Structure & Flow**
- How is the content organized?
- What are the main sections or chapters?

**Additional Notes**
- Any special features, demonstrations, or interactive elements
- Technical requirements or prerequisites mentioned

Format the summary with clear headings, bullet points for key information, and a professional but accessible tone."""

    return call_granite_api(prompt, "ibm/granite-3-3-8b-instruct", max_tokens=800)

def summarize_text(text: str) -> str:
    """Summarize text using Granite 3.3"""
    # Check if this looks like a YouTube transcript (has timestamps or is longer)
    is_youtube = len(text) > 2000 or '[' in text[:100]
    
    if is_youtube:
        # Better prompt for YouTube videos
        prompt = f"""Create a comprehensive summary of this YouTube video transcript:

{text[:3000]}

Please provide a detailed summary that includes:
1. Main topic and key themes
2. Important points and concepts discussed
3. Key takeaways for viewers
4. Overall structure and flow of the content

Format the summary in clear paragraphs with bullet points for key points."""

        return call_granite_api(prompt, "ibm/granite-3-3-8b-instruct", max_tokens=500)
    else:
        # Standard prompt for other text
        prompt = f"Provide a clear and comprehensive summary of this text in 2-3 paragraphs: {text[:2000]}"
        
        return call_granite_api(prompt, "ibm/granite-3-3-8b-instruct", max_tokens=300)

def generate_flashcards_from_text(text: str):
    """Generate flashcards from text using Granite"""
    prompt = f"Create 3 flashcards from this text: {text[:1000]}. Format: Q: [question] A: [answer]"
    
    response = call_granite_api(prompt, "ibm/granite-3-3-8b-instruct", max_tokens=300)
    
    try:
        # Try to parse the response and convert to flashcard format
        lines = response.split('\n')
        flashcards = []
        current_question = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('Q:'):
                # If we have a previous question without an answer, add it
                if current_question:
                    flashcards.append({"question": current_question, "answer": "No answer provided"})
                current_question = line.replace('Q:', '').strip()
            elif line.startswith('A:') and current_question:
                answer = line.replace('A:', '').strip()
                flashcards.append({"question": current_question, "answer": answer})
                current_question = None
        
        # If we have a question without an answer at the end
        if current_question:
            flashcards.append({"question": current_question, "answer": "No answer provided"})
        
        if flashcards:
            return flashcards
        else:
            # Fallback to simple format
            return [
                {"question": "What is the main topic?", "answer": "Based on the text provided"},
                {"question": "List one key point", "answer": "Key information from the text"}
            ]
    except Exception as e:
        print(f"Error parsing flashcards: {e}")
        # Fallback to simple format if parsing fails
        return [
            {"question": "What is the main topic?", "answer": "Based on the text provided"},
            {"question": "List one key point", "answer": "Key information from the text"}
        ]

def generate_mcq_from_text(text: str):
    """Generate multiple choice questions from text using Granite"""
    prompt = f"""Create 5 high-quality multiple choice questions from this text: {text[:2000]}

IMPORTANT: Follow this EXACT format for each question:

Q: [Write a clear, specific question about the text content]
A) [Write the first answer option]
B) [Write the second answer option]
C) [Write the third answer option]
D) [Write the fourth answer option]
Answer: [Write only A, B, C, or D]

Requirements:
- Questions must be directly related to the provided text
- All answer options must be plausible and related to the question
- Only ONE option should be correct
- The correct answer must be clearly indicated with A, B, C, or D
- Questions should test comprehension and understanding
- Avoid vague or ambiguous questions
- Make sure the answer letter matches one of the options

Example format:
Q: What is the main purpose of a computer?
A) To play games only
B) To manipulate information and data
C) To connect to the internet only
D) To store files only
Answer: B"""

    response = call_granite_api(prompt, "ibm/granite-3-3-8b-instruct", max_tokens=800)
    
    try:
        # Try to parse the response and convert to MCQ format
        lines = response.split('\n')
        mcqs = []
        current_mcq = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('Q:'):
                # If we have a previous complete MCQ, add it
                if current_mcq and current_mcq.get("question") and len(current_mcq.get("choices", [])) >= 4 and current_mcq.get("answer"):
                    mcqs.append(current_mcq)
                current_mcq = {"question": line.replace('Q:', '').strip(), "choices": [], "answer": ""}
            elif line.startswith('A)') or line.startswith('B)') or line.startswith('C)') or line.startswith('D)'):
                if current_mcq:
                    current_mcq["choices"].append(line)
            elif line.startswith('Answer:'):
                if current_mcq:
                    answer = line.replace('Answer:', '').strip()
                    # Clean up the answer to just get A, B, C, or D
                    if answer in ['A', 'B', 'C', 'D']:
                        current_mcq["answer"] = answer
                    else:
                        # Try to extract the letter from the answer
                        for char in answer:
                            if char in ['A', 'B', 'C', 'D']:
                                current_mcq["answer"] = char
                                break
        
        # Add the last MCQ if it's complete
        if current_mcq and current_mcq.get("question") and len(current_mcq.get("choices", [])) >= 4 and current_mcq.get("answer"):
            mcqs.append(current_mcq)
        
        # Validate and clean up MCQs
        valid_mcqs = []
        for mcq in mcqs:
            if (mcq.get("question") and 
                len(mcq.get("choices", [])) >= 4 and 
                mcq.get("answer") in ['A', 'B', 'C', 'D']):
                valid_mcqs.append(mcq)
        
        if valid_mcqs:
            return valid_mcqs
        else:
            # Fallback to simple format
            return [
                {
                    "question": "What is the main topic discussed in the text?",
                    "choices": ["A. General information", "B. Technical details", "C. Historical context", "D. Future predictions"],
                    "answer": "A"
                },
                {
                    "question": "Which of the following concepts is mentioned in the text?",
                    "choices": ["A. Advanced mathematics", "B. Basic principles", "C. Complex theories", "D. Scientific formulas"],
                    "answer": "B"
                }
            ]
    except Exception as e:
        print(f"Error parsing MCQs: {e}")
        print(f"Raw response: {response}")
        # Fallback to simple format if parsing fails
        return [
            {
                "question": "What is the main topic discussed in the text?",
                "choices": ["A. General information", "B. Technical details", "C. Historical context", "D. Future predictions"],
                "answer": "A"
            },
            {
                "question": "Which of the following concepts is mentioned in the text?",
                "choices": ["A. Advanced mathematics", "B. Basic principles", "C. Complex theories", "D. Scientific formulas"],
                "answer": "B"
            }
        ]

def generate_feedback(quiz_results: str):
    """Generate personalized feedback using Granite"""
    prompt = f"""Analyze these quiz results and provide personalized feedback:

Quiz Results: {quiz_results}

Please provide constructive feedback that includes:
1. What the student did well (strengths)
2. Areas for improvement (weaknesses) 
3. Specific study suggestions and resources
4. Encouragement and motivation

Format your response in a friendly, supportive tone with clear sections."""

    return call_granite_api(prompt, "ibm/granite-3-3-8b-instruct", max_tokens=400) 