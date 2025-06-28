
## Testing the API

### 1. Interactive API Documentation
Visit **http://127.0.0.1:8000/docs** for interactive API testing.

### 2. Test with curl

#### Test Summarization:
```bash
curl -X POST "http://127.0.0.1:8000/summarize" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions without being explicitly programmed. It uses algorithms and statistical models to analyze and draw inferences from patterns in data.&token=test"
```

#### Test Flashcard Generation:
```bash
curl -X POST "http://127.0.0.1:8000/generate_flashcards" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions without being explicitly programmed. It uses algorithms and statistical models to analyze and draw inferences from patterns in data.&token=test"
```

#### Test MCQ Generation:
```bash
curl -X POST "http://127.0.0.1:8000/generate_mcq" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions without being explicitly programmed. It uses algorithms and statistical models to analyze and draw inferences from patterns in data.&token=test"
```

### 3. Expected Responses

#### Summarization Response:
```json
{
  "summary": "Machine learning, a branch of AI, allows computers to autonomously learn from data patterns and make decisions, employing algorithms and statistical models for analysis and inference."
}
```

#### Flashcard Response:
```json
{
  "flashcards": [
    {
      "question": "What is machine learning?",
      "answer": "Machine learning is a subset of artificial intelligence that allows computers to learn and make decisions autonomously, using algorithms and statistical models for pattern recognition in data."
    },
    {
      "question": "How does machine learning differ from traditional programming?",
      "answer": "Unlike traditional programming where explicit instructions are given to the computer, machine learning enables computers to learn and make decisions based on patterns in data through algorithms and statistical models."
    }
  ]
}
```

#### MCQ Response:
```json
{
  "mcqs": [
    {
      "question": "What is machine learning classified as?",
      "choices": [
        "A) A branch of mathematics",
        "B) A subset of artificial intelligence", 
        "C) A type of hardware",
        "D) A form of energy"
      ],
      "answer": "B"
    }
  ]
}
```
