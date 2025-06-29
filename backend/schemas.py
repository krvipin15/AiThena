from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class ChapterSummary(BaseModel):
    title: str
    summary: str

class SummaryResponse(BaseModel):
    summaries: List[Dict[str, str]]

class YouTubeResponse(BaseModel):
    transcript: str
    summary: str
    video_info: Dict[str, Any]

class SummarizeResponse(BaseModel):
    summary: str

class StoreResultResponse(BaseModel):
    status: str

class Flashcard(BaseModel):
    question: str
    answer: str

class FlashcardResponse(BaseModel):
    flashcards: List[Dict[str, str]]

class MCQ(BaseModel):
    question: str
    choices: list[str]
    answer: str

class MCQResponse(BaseModel):
    mcqs: List[Dict[str, Any]]

class FeedbackResponse(BaseModel):
    feedback: str

class AuthRequest(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    success: bool
    message: str
    user_id: Optional[str] = None

class YouTubeTranscriptResponse(BaseModel):
    success: bool
    transcript: str = None
    summary: str = None
    video_info: Dict[str, Any] = None
    error: str = None 
