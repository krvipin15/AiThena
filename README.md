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
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the example environment file and add your credentials:

```bash
cp env.example .env
```

Then edit the `.env` file with your credentials:

```bash
# Granite API Configuration
GRANITE_API_KEY=your_ibm_api_key_here
GRANITE_API_URL=https://us-south.ml.cloud.ibm.com
PROJECT_ID=your_project_id_here
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

### 5. Run the Backend Server
```bash
uvicorn backend.main:app --reload
```

The server will start at: **http://127.0.0.1:8000**

---

## API Endpoints

### Authentication
- All endpoints require email and password authentication using bcrypt.
- User data is stored in SQLite3 database.

### Authentication Endpoints
- `POST /register` — Register a new user with email and password.
- `POST /login` — Authenticate user and get user ID.

### PDF Processing
- `POST /upload_pdf` — Upload a PDF, returns chapter summaries.

### YouTube Processing
- `POST /process_youtube` — Submit a YouTube link, returns transcript and summary.
- `POST /youtube_transcript` — Get YouTube transcript with timestamps.

### Summarization
- `POST /summarize` — Summarize arbitrary text.

### Flashcards & MCQ
- `POST /generate_flashcards` — Generate flashcards from text.
- `POST /generate_mcq` — Generate MCQs from text.

### Feedback
- `POST /feedback` — Analyze quiz results and get personalized feedback.

### Store Results
- `POST /store_result` — Store quiz/user results in SQLite database.

---

## Environment Variables
- `GRANITE_API_KEY` — Your IBM watsonx.ai API key
- `GRANITE_API_URL` — IBM watsonx.ai endpoint (default: `https://us-south.ml.cloud.ibm.com`)
- `PROJECT_ID` — Your IBM watsonx.ai project ID

**Security Note:** For production, always set these environment variables instead of using the default values in the code.

---

## Features

### ✅ Working Features
- **Real Granite 3.3 Integration** - Using `ibm/granite-3-3-8b-instruct` model
- **Concise Summarization** - Generate brief, accurate summaries
- **Flashcard Generation** - Create high-quality Q&A flashcards
- **MCQ Generation** - Produce well-structured multiple choice questions
- **Adaptive Feedback** - Analyze quiz results and provide personalized feedback with study suggestions
- **PDF Processing** - Upload and process PDFs with Docling
- **YouTube Integration** - Get transcripts and generate summaries from YouTube videos
- **Bcrypt Authentication** - Secure password hashing and SQLite3 user storage
- **User Management** - Register, login, and store user data securely

### 🔄 In Development
- **Frontend UI** - User interface for all features
- **TTS Integration** - Audio summaries
- **Progress Dashboard** - User performance tracking

---

## Notes
- PDF parsing uses Docling (with PyPDF2 fallback).
- Granite API integration uses IAM token exchange for secure authentication.
- All user data and feedback are stored in SQLite3 database.
- YouTube transcripts are automatically saved to `data/youtube_transcript/` directory.
- The backend includes comprehensive error handling and fallbacks.

---

## Testing

For comprehensive API testing examples and expected responses, see [test_response.md](test_response.md).

---

## Security

### ⚠️ Important Security Notes:

1. **Never commit your `.env` file** - It contains sensitive API keys
2. **Use the `env.example` template** - Copy it to `.env` and fill in your credentials
3. **Keep your API keys private** - Don't share them in code, logs, or public repositories
4. **Rotate keys regularly** - Update your IBM watsonx.ai API keys periodically
5. **Use environment variables** - Never hardcode credentials in your source code

### Environment Variables:
- `GRANITE_API_KEY` — Your IBM watsonx.ai API key (REQUIRED)
- `GRANITE_API_URL` — IBM watsonx.ai endpoint (default: `https://us-south.ml.cloud.ibm.com`)
- `PROJECT_ID` — Your IBM watsonx.ai project ID (REQUIRED)

---

## Troubleshooting

### Common Issues:

1. **401 Unauthorized Error:**
   - Check your `GRANITE_API_KEY` and `PROJECT_ID` in `.env`
   - Ensure your IBM watsonx.ai project is active
   - Verify your email and password for authentication

2. **Module Not Found Errors:**
   - Make sure you're in the virtual environment: `source venv/bin/activate`
   - Install dependencies: `pip install -r requirements.txt`

3. **YouTube Transcript Errors:**
   - Ensure the YouTube video has available captions/transcripts
   - Check if the video is public and accessible

4. **Empty API Responses:**
   - Check backend logs for detailed error messages
   - Verify your IBM watsonx.ai project has access to Granite models

---

## License
MIT License - see LICENSE file for details.
