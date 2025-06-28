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

### 4. Set Up Environment Variables

Create a `.env` file in the project root with your credentials:

```bash
# Granite API Configuration
GRANITE_API_KEY=your_ibm_api_key_here
GRANITE_API_URL=https://us-south.ml.cloud.ibm.com
PROJECT_ID=your_project_id_here

# Firebase Configuration
FIREBASE_KEY_PATH=/Users/ymk/Desktop/AiThena/backend/firebase_service_account.json
```

#### How to Get IBM Watsonx.ai Credentials:

1. **Go to [IBM Watsonx.ai](https://www.ibm.com/products/watsonx)**
2. **Sign up/Login** to your IBM Cloud account
3. **Create a Project** in the watsonx.ai dashboard
4. **Get API Key:**
   - Go to Project Settings → API Keys
   - Click "Create" or "View" to generate an API key
   - Copy the API key
5. **Get Project ID:**
   - In your project dashboard, find the Project ID
   - Copy the Project ID
6. **Add to .env file** as shown above

### 5. Add Firebase Service Account
- Place your `firebase_service_account.json` in the `backend/` directory, or set the `FIREBASE_KEY_PATH` environment variable.

### 6. Run the Backend Server
```bash
uvicorn backend.main:app --reload
```

The server will start at: **http://127.0.0.1:8000**

---

## API Endpoints

### Authentication
- All endpoints require a Firebase Auth token (pass as `token` in form data).
- For testing, you can use `token=test` (authentication is temporarily disabled for development).

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
- `GRANITE_API_KEY` — Your IBM watsonx.ai API key
- `GRANITE_API_URL` — IBM watsonx.ai endpoint (default: `https://us-south.ml.cloud.ibm.com`)
- `PROJECT_ID` — Your IBM watsonx.ai project ID
- `FIREBASE_KEY_PATH` — Path to Firebase service account key (default: `backend/firebase_service_account.json`)

**Security Note:** For production, always set these environment variables instead of using the default values in the code.

---

## Features

### ✅ Working Features
- **Real Granite 3.3 Integration** - Using `ibm/granite-3-3-8b-instruct` model
- **Concise Summarization** - Generate brief, accurate summaries
- **Flashcard Generation** - Create high-quality Q&A flashcards
- **MCQ Generation** - Produce well-structured multiple choice questions
- **PDF Processing** - Upload and process PDFs with Docling
- **YouTube Integration** - Process YouTube links (transcription placeholder)
- **Firebase Integration** - Authentication and data storage ready

### 🔄 In Development
- **YouTube Transcription** - Real speech-to-text integration
- **Frontend UI** - User interface for all features
- **TTS Integration** - Audio summaries
- **Progress Dashboard** - User performance tracking

---

## Notes
- PDF parsing uses Docling (with PyPDF2 fallback).
- Granite API integration uses IAM token exchange for secure authentication.
- All user data and feedback are stored in Firebase Firestore.
- The backend includes comprehensive error handling and fallbacks.

---

## Troubleshooting

### Common Issues:

1. **401 Unauthorized Error:**
   - Check your `GRANITE_API_KEY` and `PROJECT_ID` in `.env`
   - Ensure your IBM watsonx.ai project is active

2. **Module Not Found Errors:**
   - Make sure you're in the virtual environment: `source venv/bin/activate`
   - Install dependencies: `pip install -r backend/requirements.txt`

3. **Firebase Errors:**
   - Ensure `firebase_service_account.json` is in the `backend/` directory
   - Check the file path in `FIREBASE_KEY_PATH`

4. **Empty API Responses:**
   - Check backend logs for detailed error messages
   - Verify your IBM watsonx.ai project has access to Granite models

---

## License
MIT License - see LICENSE file for details.
