# AiThena API Testing Guide

This document contains all test examples and expected responses for the AiThena backend API.

---

## Quick Start Testing

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

#### Test Adaptive Feedback:
```bash
curl -X POST "http://127.0.0.1:8000/feedback" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "user_id=test_user&quiz_results=Student scored 7/10 on Machine Learning quiz. Correct answers: Basic concepts, algorithms, supervised learning. Incorrect: Neural networks, deep learning concepts. Time taken: 15 minutes.&token=test"
```

#### Test Low Score Feedback:
```bash
curl -X POST "http://127.0.0.1:8000/feedback" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "user_id=test_user2&quiz_results=Student scored 3/10 on Physics quiz. Correct answers: Basic motion concepts. Incorrect: Newton's laws, energy conservation, momentum, thermodynamics, wave properties, electricity, magnetism, optics. Time taken: 8 minutes (very fast).&token=test"
```

---

## Expected Responses

### 1. Summarization Response:
```json
{
  "summary": "Machine learning, a branch of AI, allows computers to autonomously learn from data patterns and make decisions, employing algorithms and statistical models for analysis and inference."
}
```

### 2. Flashcard Response:
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

### 3. MCQ Response:
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

### 4. Adaptive Feedback Response (High Score):
```json
{
  "feedback": "---\n\n**Feedback Section 1: Strengths**\n\nYou've demonstrated a solid grasp of fundamental machine learning concepts such as basic principles, algorithms, and supervised learning. This is an excellent foundation to build upon! Keep up the great work in understanding these core ideas.\n\n---\n\n**Feedback Section 2: Weaknesses**\n\nWhile you've shown strength in foundational knowledge, there's room for growth in two key areas: neural networks and deep learning concepts. These topics are crucial for a comprehensive understanding of modern machine learning techniques. Let's focus on enhancing your expertise here.\n\n---\n\n**Feedback Section 3: Study Suggestions & Resources**\n\n*Neural Networks:*\n- *Book*: \"Deep Learning\" by Ian Goodfellow, Yoshua Bengio, and Aaron Courville - Offers a thorough introduction to neural networks and deep learning.\n- *Online Course*: Andrew Ng's \"Neural Networks and Deep Learning\" on Coursera - Provides practical insights through hands-on projects.\n\n*Deep Learning Concepts:*\n- *Online Article Series*: \"Understanding Deep Learning Requirements for Edge Deployment\" by Merlion Team - Gives a clear overview of essential deep learning concepts.\n- *YouTube Channel*: 3Blue1Brown - Offers visually engaging explanations of complex topics like neural networks and backpropagation.\n\nRemember, consistent practice and application are vital. Try implementing simple neural network models using libraries like TensorFlow or PyTorch to reinforce your understanding.\n\n---\n\n**Feedback Section 4: Encouragement & Motivation**\n\nDon't be discouraged by the areas needing improvement; instead, view them as exciting opportunities to expand your skill set. Machine learning is a rapidly evolving field, and mastering neural networks and deep learning will open doors to advanced applications and career opportunities."
}
```

### 5. Adaptive Feedback Response (Low Score):
```json
{
  "feedback": "---\n\n**Feedback Section 1: Strengths**\n\nYou've demonstrated a solid grasp of *basic motion concepts*! This is a fantastic foundation for understanding more complex physics topics. Keep up the great work in mastering these fundamental principles.\n\n---\n\n**Feedback Section 2: Weaknesses**\n\nIt seems there are several areas where you could benefit from further review and practice. These include:\n- *Newton's laws*: Understanding these foundational principles will help you tackle problems involving forces and motion.\n- *Energy conservation*: Grasping this concept is crucial for solving problems related to energy transformations.\n- *Momentum*: A strong command of momentum will aid in analyzing collisions and impetus.\n- *Thermodynamics*: Familiarity with thermodynamic principles will enhance your ability to understand heat transfer and engine efficiency.\n- *Wave properties*: Knowledge of waves will enable you to analyze various phenomena like sound, light, and seismic activity.\n- *Electricity*: Comprehending electrical principles is essential for working with circuits and electronic devices.\n- *Magnetism*: Magnetic forces play a significant role in many technologies; gaining proficiency here will be beneficial.\n- *Optics*: Optical concepts are vital for understanding how lenses, mirrors, and other optical instruments function.\n\n---\n\n**Feedback Section 3: Study Suggestions & Resources**\n\n1. *Khan Academy*: This platform offers comprehensive video lessons and practice exercises covering all the topics mentioned above. Start by reviewing the content related to each weakness area.\n2. *Physics Classroom*: This website provides detailed explanations and interactive tutorials for various physics concepts. Use it to reinforce your understanding of the weaker areas.\n3. *MIT OpenCourseWare*: Access free physics courses from MIT to get a deeper understanding of complex topics.\n4. *Practice Problems*: Work through step-by-step problems for each topic to build confidence and understanding.\n\n---\n\n**Feedback Section 4: Encouragement & Motivation**\n\nRemember, every expert was once a beginner! Physics can be challenging, but with consistent effort and the right resources, you can master these concepts. Focus on understanding the fundamental principles, and don't hesitate to seek help when needed. Your foundation in basic motion concepts shows you have the ability to learn and grow."
}
```

---

## Testing Different Scenarios

### Test with Different Subjects:
```bash
# Biology Quiz
curl -X POST "http://127.0.0.1:8000/feedback" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "user_id=test_user3&quiz_results=Student scored 8/10 on Biology quiz. Correct answers: Cell structure, photosynthesis, genetics basics, evolution. Incorrect: DNA replication details, protein synthesis. Time taken: 20 minutes.&token=test"

# Math Quiz
curl -X POST "http://127.0.0.1:8000/feedback" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "user_id=test_user4&quiz_results=Student scored 5/10 on Calculus quiz. Correct answers: Basic derivatives, limits. Incorrect: Integration, chain rule, optimization, related rates. Time taken: 25 minutes.&token=test"
```

### Test with Different Performance Levels:
```bash
# Perfect Score
curl -X POST "http://127.0.0.1:8000/feedback" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "user_id=test_user5&quiz_results=Student scored 10/10 on Chemistry quiz. All answers correct: Atomic structure, chemical bonding, reactions, stoichiometry, thermodynamics. Time taken: 18 minutes.&token=test"

# Very Low Score
curl -X POST "http://127.0.0.1:8000/feedback" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "user_id=test_user6&quiz_results=Student scored 1/10 on History quiz. Correct: One basic fact. Incorrect: All major events, dates, figures, causes, effects. Time taken: 5 minutes (very rushed).&token=test"
```

---

## Error Testing

### Test with Invalid Token:
```bash
curl -X POST "http://127.0.0.1:8000/summarize" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=Test text&token=invalid_token"
```

### Test with Missing Parameters:
```bash
curl -X POST "http://127.0.0.1:8000/feedback" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "user_id=test_user&token=test"
```

### Test with Empty Text:
```bash
curl -X POST "http://127.0.0.1:8000/summarize" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=&token=test"
```

---

## Performance Testing

### Test with Long Text:
```bash
curl -X POST "http://127.0.0.1:8000/summarize" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "text=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 1000 | head -n 1)&token=test"
```

### Test Concurrent Requests:
```bash
# Run multiple requests simultaneously
for i in {1..5}; do
  curl -X POST "http://127.0.0.1:8000/summarize" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "text=Test text $i&token=test" &
done
wait
```

---

## Notes

- All endpoints require a `token` parameter (use `token=test` for development)
- Replace `token=test` with valid Firebase authentication tokens
- Responses are in JSON format
- The adaptive feedback system analyzes performance patterns and provides personalized guidance
- Error responses include appropriate HTTP status codes and error messages

