# AiThena

AiThena is a personalized AI tutor platform powered by IBM watsonx Granite 3.3 and FastAPI. It generates adaptive study materials—summaries, flashcards, MCQs, and feedback—from PDFs and YouTube videos, with secure user authentication and a modern Streamlit frontend.

---

## Key Features

- **AI Summarization:** Generate concise, chapter-wise summaries from PDFs and YouTube transcripts.
- **Flashcards & MCQs:** Instantly create high-quality flashcards and multiple-choice quizzes from any text.
- **YouTube Integration:** Extract and summarize transcripts from YouTube videos.
- **Adaptive Feedback:** Get personalized study feedback based on quiz results.
- **User Authentication:** Secure registration and login with bcrypt and SQLite3.
- **Progress Tracking:** Monitor your learning journey and quiz performance.
- **Modern UI:** Clean, responsive Streamlit interface with session management.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repo-url>
cd AiThena
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Copy the example file and add your IBM watsonx credentials:

```bash
cp env.example .env
```

Edit `.env` and set:

```
GRANITE_API_KEY=your_ibm_api_key
GRANITE_API_URL=https://us-south.ml.cloud.ibm.com
PROJECT_ID=your_project_id
```

### 5. Start the Backend

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### 6. Start the Frontend

```bash
cd frontend
streamlit run app.py
```

### 7. Access the App

- Frontend: [http://localhost:8501](http://localhost:8501)
- Backend API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Project Structure

```
AiThena/
├── backend/         # FastAPI backend (auth, AI, processing)
├── frontend/        # Streamlit frontend (UI, pages)
├── data/            # User DB and transcripts
├── requirements.txt # Python dependencies
└── README.md
```

---

## Security Notes

- **Never commit your `.env` file** (contains API keys)
- **Passwords are securely hashed** with bcrypt
- **All user data** is stored in a single SQLite3 database (`data/auth_db/users.db`)

---

## License

MIT License
