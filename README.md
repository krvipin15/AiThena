# AiThena
Personalized AI tutor, built with IBM Granite 3.3 &amp; Watsonx.ai. This adaptive tutor generates chapter-wise PDF summaries, YouTube notes, flashcards, and MCQ quizzes.

---

## Backend Setup & Usage

### 1. Clone the Repository
```bash
git clone <repo-url>
cd AiThena
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Add Firebase Service Account
- Place your `firebase_service_account.json` in the `backend/` directory, or set the `FIREBASE_KEY_PATH` environment variable.
- **To set the environment variable (recommended for security):**
  ```bash
  export FIREBASE_KEY_PATH=/Users/ymk/Desktop/AiThena/backend/firebase_service_account.json
  ```
  (Replace with your actual path if different.)
- You can add this line to your `~/.zshrc` or `~/.bashrc` for convenience.

### 5. Run the Backend Server
```bash
uvicorn backend.main:app --reload
```

---

## API Endpoints

### Authentication
- All endpoints require a Firebase Auth token (pass as `token` in form data).

### PDF Processing
- `POST /upload_pdf` — Upload a PDF, returns chapter summaries.

### YouTube Processing
- `POST /process_youtube` — Submit a YouTube link, returns transcript and summary.

### Summarization
- `POST /summarize` — Summarize arbitrary text.

### Flashcards & MCQ
- `POST /generate_flashcards` — Generate flashcards from text.
- `POST /generate_mcq` — Generate MCQs from text.

### Feedback
- `POST /feedback` — Analyze quiz results and get personalized feedback.

### Store Results
- `POST /store_result` — Store quiz/user results in Firestore.

---

## Environment Variables
- `FIREBASE_KEY_PATH` — Path to Firebase service account key (default: `backend/firebase_service_account.json`).
  - Example:
    ```bash
    export FIREBASE_KEY_PATH=/Users/ymk/Desktop/AiThena/backend/firebase_service_account.json
    ```
- `GRANITE_API_KEY` and `GRANITE_API_URL` — (For future Granite integration)

---

## Notes
- PDF parsing uses Docling (with PyPDF2 fallback).
- Granite API integration is a placeholder; update `backend/granite.py` when you have credentials.
- All user data and feedback are stored in Firebase Firestore.

---

## Frontend
- (Frontend setup instructions go here if/when available)
