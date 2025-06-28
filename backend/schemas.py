from pydantic import BaseModel
from typing import List, Dict, Any

class ChapterSummary(BaseModel):
    title: str
    summary: str

class SummaryResponse(BaseModel):
    summaries: List[ChapterSummary]

class YouTubeResponse(BaseModel):
    transcript: str
    summary: str

class SummarizeResponse(BaseModel):
    summary: str

class StoreResultResponse(BaseModel):
    status: str 

class Flashcard(BaseModel):
    question: str
    answer: str

class FlashcardResponse(BaseModel):
    flashcards: list[Flashcard]

class MCQ(BaseModel):
    question: str
    choices: list[str]
    answer: str

class MCQResponse(BaseModel):
    mcqs: list[MCQ]

class FeedbackResponse(BaseModel):
    feedback: str 
