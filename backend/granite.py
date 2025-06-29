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

def summarize_text(text: str) -> str:
    """Summarize text using Granite 3.3"""
    prompt = f"Provide a brief, concise summary of this text in 1-2 sentences: {text[:1500]}"
    
    return call_granite_api(prompt, "ibm/granite-3-3-8b-instruct", max_tokens=100)

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
    prompt = f"Create 2 multiple choice questions from this text: {text[:1000]}. Format each as: Q: [question] A) [option] B) [option] C) [option] D) [option] Answer: [A/B/C/D]"
    
    response = call_granite_api(prompt, "ibm/granite-3-3-8b-instruct", max_tokens=400)
    
    try:
        # Try to parse the response and convert to MCQ format
        lines = response.split('\n')
        mcqs = []
        current_mcq = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('Q:'):
                if current_mcq:
                    mcqs.append(current_mcq)
                current_mcq = {"question": line.replace('Q:', '').strip(), "choices": [], "answer": ""}
            elif line.startswith('A)') or line.startswith('B)') or line.startswith('C)') or line.startswith('D)'):
                if current_mcq:
                    current_mcq["choices"].append(line)
            elif line.startswith('Answer:'):
                if current_mcq:
                    current_mcq["answer"] = line.replace('Answer:', '').strip()
        
        if current_mcq:
            mcqs.append(current_mcq)
        
        if mcqs:
            return mcqs
        else:
            # Fallback to simple format
            return [
                {
                    "question": "What is the main topic of this text?",
                    "choices": ["A. Topic A", "B. Topic B", "C. Topic C", "D. Topic D"],
                    "answer": "A"
                }
            ]
    except:
        # Fallback to simple format if parsing fails
        return [
            {
                "question": "What is the main topic of this text?",
                "choices": ["A. Topic A", "B. Topic B", "C. Topic C", "D. Topic D"],
                "answer": "A"
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