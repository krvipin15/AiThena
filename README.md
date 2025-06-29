# AiThena

AiThena is a personalized AI tutor platform powered by IBM watsonx Granite 3.3 and FastAPI. It generates adaptive study materials—summaries, flashcards, MCQs, and feedback—from PDFs and YouTube videos, with secure user authentication and a modern Streamlit frontend.

---

## 🌟 Key Features

- **📄 PDF Processing**: AI-generated chapter summaries from textbooks
- **🎥 YouTube Integration**: Extract and summarize video transcripts
- **✍️ Smart Summarization**: Concise summaries from any text content
- **🎯 AI Flashcards**: Interactive study cards generated automatically
- **📝 Quiz Generation**: Multiple-choice questions with instant feedback
- **📊 Personalized Feedback**: Adaptive learning recommendations
- **🔐 Secure Authentication**: User registration with bcrypt encryption

---

## 🏗️ Project Structure
```
AiThena/
├── backend/         # FastAPI backend (auth, AI, processing)
├── frontend/        # Streamlit frontend (UI, pages)
├── data/            # User DB and transcripts
├── requirements.txt # Python dependencies
└── README.md
```
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

## 🎯 Usage Guide

1. **Register/Login**: Create account or login with existing credentials
2. **Upload Content**:
   - 📄 Upload PDF files for chapter summaries
   - 🎥 Paste YouTube URLs for video analysis
   - ✍️ Input custom text for summarization
3. **Generate Materials**:
   - 🎯 Create flashcards from any content source
   - 📝 Generate quiz questions automatically
4. **Learn & Improve**:
   - Take quizzes to test knowledge
   - Get AI-powered personalized feedback
   - Track learning progress

---

## 🛠️ Technology Stack

- **AI Engine**: IBM Granite 3.3 (Watsonx.ai)
- **Backend**: FastAPI, Python 3.8+
- **Database**: SQLite3 with bcrypt encryption
- **Frontend**: Streamlit (Python-based)
- **APIs**: IBM Watsonx.ai REST APIs
- **Security**: bcrypt password hashing, session management

---

## 🔐 Security Features

- Secure user authentication with bcrypt
- Environment-based API key management
- Input validation and sanitization
- Session-based security
- SQLite3 with prepared statements

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🏆 Hackathon Submission

**Built for IBM AI & Automation Unpacked Hackathon**

_Transforming education through intelligent AI automation using IBM Granite 3.3_

---

## 📞 Support

For questions or support, please open an issue in the GitHub repository.

**Made with ❤️ using IBM Granite 3.3 & Watsonx.ai**
