from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .firebase import verify_firebase_token, store_user_result, store_user_feedback
from .processors import extract_text_and_chapters, download_youtube_audio, transcribe_audio
from .granite import summarize_text, generate_flashcards_from_text, generate_mcq_from_text, generate_feedback
from .schemas import SummaryResponse, YouTubeResponse, SummarizeResponse, StoreResultResponse, FlashcardResponse, MCQResponse, FeedbackResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "AiThena backend running"}

@app.post("/upload_pdf", response_model=SummaryResponse)
async def upload_pdf(file: UploadFile = File(...), token: str = Form("test")):
    # verify_firebase_token(token)  # Temporarily commented for testing
    chapters = extract_text_and_chapters(file)
    summaries = [
        {"title": ch["title"], "summary": summarize_text(ch["content"])}
        for ch in chapters
    ]
    return {"summaries": summaries}

@app.post("/process_youtube", response_model=YouTubeResponse)
async def process_youtube(youtube_url: str = Form(...), token: str = Form("test")):
    # verify_firebase_token(token)  # Temporarily commented for testing
    audio_path = download_youtube_audio(youtube_url)
    if not audio_path:
        raise HTTPException(status_code=400, detail="Failed to download audio")
    transcript = transcribe_audio(audio_path)
    summary = summarize_text(transcript)
    return {"transcript": transcript, "summary": summary}

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(text: str = Form(...), token: str = Form("test")):
    # verify_firebase_token(token)  # Temporarily commented for testing
    summary = summarize_text(text)
    return {"summary": summary}

@app.post("/store_result", response_model=StoreResultResponse)
async def store_result(user_id: str = Form(...), result: str = Form(...), token: str = Form("test")):
    # verify_firebase_token(token)  # Temporarily commented for testing
    store_user_result(user_id, {"result": result})
    return {"status": "result stored"}

@app.post("/generate_flashcards", response_model=FlashcardResponse)
async def generate_flashcards(text: str = Form(...), token: str = Form("test")):
    # verify_firebase_token(token)  # Temporarily commented for testing
    flashcards = generate_flashcards_from_text(text)
    return {"flashcards": flashcards}

@app.post("/generate_mcq", response_model=MCQResponse)
async def generate_mcq(text: str = Form(...), token: str = Form("test")):
    # verify_firebase_token(token)  # Temporarily commented for testing
    mcqs = generate_mcq_from_text(text)
    return {"mcqs": mcqs}

@app.post("/feedback", response_model=FeedbackResponse)
async def feedback(user_id: str = Form(...), quiz_results: str = Form(...), token: str = Form(...)):
    # verify_firebase_token(token)  # Temporarily commented for testing
    try:
        feedback_text = generate_feedback(quiz_results)
        # Try to store feedback, but don't fail if Firebase is not configured
        try:
            store_user_feedback(user_id, feedback_text)
        except Exception as e:
            print(f"Warning: Could not store feedback in Firebase: {e}")
        return {"feedback": feedback_text}
    except Exception as e:
        print(f"Error generating feedback: {e}")
        return {"feedback": "Sorry, there was an error generating feedback. Please try again."} 