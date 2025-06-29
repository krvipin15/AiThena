from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .auth import register_user, authenticate_user, get_user_id, store_user_result, store_user_feedback
from .processors import extract_text_and_chapters
from .granite import summarize_text, generate_flashcards_from_text, generate_mcq_from_text, generate_feedback
from .youtube_processor import youtube_processor
from .schemas import (
    SummaryResponse, YouTubeTranscriptResponse, SummarizeResponse, 
    StoreResultResponse, FlashcardResponse, MCQResponse, FeedbackResponse,
    AuthRequest, AuthResponse
)

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

# Authentication endpoints
@app.post("/register", response_model=AuthResponse)
async def register(request: AuthRequest):
    success, message = register_user(request.email, request.password)
    user_email = get_user_id(request.email) if success else None
    return AuthResponse(success=success, message=message, user_id=user_email)

@app.post("/login", response_model=AuthResponse)
async def login(request: AuthRequest):
    success, message = authenticate_user(request.email, request.password)
    user_email = get_user_id(request.email) if success else None
    return AuthResponse(success=success, message=message, user_id=user_email)

@app.post("/upload_pdf", response_model=SummaryResponse)
async def upload_pdf(file: UploadFile = File(...), email: str = Form(...), password: str = Form(...)):
    # Authenticate user
    success, message = authenticate_user(email, password)
    if not success:
        raise HTTPException(status_code=401, detail=message)
    
    chapters = extract_text_and_chapters(file)
    summaries = [
        {"title": ch["title"], "summary": summarize_text(ch["content"])}
        for ch in chapters
    ]
    return {"summaries": summaries}

@app.post("/process_youtube", response_model=YouTubeTranscriptResponse)
async def process_youtube(youtube_url: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # Authenticate user
    success, message = authenticate_user(email, password)
    if not success:
        raise HTTPException(status_code=401, detail=message)
    
    # Get video info
    info_success, video_info = youtube_processor.get_video_info(youtube_url)
    if not info_success:
        return YouTubeTranscriptResponse(success=False, error=video_info.get("error", "Failed to get video info"))
    
    # Get transcript
    transcript_success, transcript = youtube_processor.get_transcript(youtube_url)
    if not transcript_success:
        return YouTubeTranscriptResponse(success=False, error=transcript)
    
    # Generate summary
    summary = summarize_text(transcript)
    
    return YouTubeTranscriptResponse(
        success=True,
        transcript=transcript,
        summary=summary,
        video_info=video_info
    )

@app.post("/youtube_transcript", response_model=YouTubeTranscriptResponse)
async def get_youtube_transcript(youtube_url: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # Authenticate user
    success, message = authenticate_user(email, password)
    if not success:
        raise HTTPException(status_code=401, detail=message)
    
    # Get transcript with timestamps
    transcript_success, transcript = youtube_processor.get_transcript_with_timestamps(youtube_url)
    if not transcript_success:
        return YouTubeTranscriptResponse(success=False, error=transcript)
    
    # Get video info
    info_success, video_info = youtube_processor.get_video_info(youtube_url)
    
    return YouTubeTranscriptResponse(
        success=True,
        transcript=transcript,
        video_info=video_info if info_success else {}
    )

@app.post("/summarize", response_model=SummarizeResponse)
async def summarize(text: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # Authenticate user
    success, message = authenticate_user(email, password)
    if not success:
        raise HTTPException(status_code=401, detail=message)
    
    summary = summarize_text(text)
    return {"summary": summary}

@app.post("/store_result", response_model=StoreResultResponse)
async def store_result(email: str = Form(...), password: str = Form(...), result: str = Form(...)):
    # Authenticate user
    success, message = authenticate_user(email, password)
    if not success:
        raise HTTPException(status_code=401, detail=message)
    
    store_user_result(email, {"result": result})
    return {"status": "result stored"}

@app.post("/generate_flashcards", response_model=FlashcardResponse)
async def generate_flashcards(text: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # Authenticate user
    success, message = authenticate_user(email, password)
    if not success:
        raise HTTPException(status_code=401, detail=message)
    
    flashcards = generate_flashcards_from_text(text)
    return {"flashcards": flashcards}

@app.post("/generate_mcq", response_model=MCQResponse)
async def generate_mcq(text: str = Form(...), email: str = Form(...), password: str = Form(...)):
    # Authenticate user
    success, message = authenticate_user(email, password)
    if not success:
        raise HTTPException(status_code=401, detail=message)
    
    mcqs = generate_mcq_from_text(text)
    return {"mcqs": mcqs}

@app.post("/feedback", response_model=FeedbackResponse)
async def feedback(email: str = Form(...), password: str = Form(...), quiz_results: str = Form(...)):
    # Authenticate user
    success, message = authenticate_user(email, password)
    if not success:
        raise HTTPException(status_code=401, detail=message)
    
    try:
        feedback_text = generate_feedback(quiz_results)
        # Store feedback
        store_user_feedback(email, feedback_text)
        return {"feedback": feedback_text}
    except Exception as e:
        print(f"Error generating feedback: {e}")
        return {"feedback": "Sorry, there was an error generating feedback. Please try again."} 