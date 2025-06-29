# 🤖 AiThena - AI-Powered Learning Platform

> **Personalized AI tutor powered by IBM Granite 3.3 & Watsonx.ai**

AiThena transforms learning through intelligent AI-driven study materials generation. Upload PDFs, analyze YouTube videos, and get personalized flashcards, quizzes, and feedback powered by IBM's latest Granite 3.3 models.

---

## 🌟 Key Features

- **📄 PDF Processing**: AI-generated chapter summaries from textbooks
- **🎥 YouTube Integration**: Extract and summarize video transcripts
- **✍️ Smart Summarization**: Concise summaries from any text content
- **🎯 AI Flashcards**: Interactive study cards generated automatically
- **📝 Quiz Generation**: Multiple-choice questions with instant feedback
- **📊 Personalized Feedback**: Adaptive learning recommendations
- **🔐 Secure Authentication**: User registration with bcrypt encryption
- **🎨 Modern UI**: Two frontend options - Web & Streamlit

---

## 🏗️ Project Structure

```
AiThena/
├── backend/                 # FastAPI backend services
│   ├── main.py             # Main FastAPI application
│   ├── granite.py          # IBM Granite 3.3 integration
│   ├── auth.py             # Authentication logic
│   └── database.py         # SQLite database operations
├── frontend-web/           # Modern web frontend (HTML/CSS/JS)
│   ├── dashboard.html      # Main dashboard interface
│   ├── login.html         # User authentication
│   ├── js/dashboard.js    # Frontend JavaScript logic
│   └── assets/            # Logo and static assets
├── frontend/              # Streamlit frontend (Alternative)
│   └── app.py            # Streamlit application
├── data/                 # Generated content storage
├── .env.example         # Environment variables template
└── requirements.txt     # Python dependencies
```

---

## 🚀 Quick Setup

### Prerequisites

- Python 3.8+
- IBM Cloud account with Watsonx.ai access
- 32GB RAM recommended for optimal performance

### 1. Clone Repository

```bash
git clone https://github.com/krvipin15/AiThena.git
cd AiThena
```

### 2. Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure IBM Granite

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your IBM credentials:
# GRANITE_API_KEY=your_ibm_api_key
# GRANITE_API_URL=https://us-south.ml.cloud.ibm.com
# PROJECT_ID=your_project_id
```

### 4. Start Backend

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

### 5. Choose Your Frontend

#### Option A: Modern Web Interface (Recommended)

```bash
# Open in browser
http://localhost:8000/index.html
```

#### Option B: Streamlit Interface

```bash
cd frontend
streamlit run app.py
```

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
- **Frontend Options**:
  - Modern Web (HTML5/CSS3/JavaScript)
  - Streamlit (Python-based)
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

## 📊 IBM Granite 3.3 Integration

AiThena leverages IBM's latest Granite 3.3 models for:

- **Text Summarization**: Advanced document processing
- **Question Generation**: Intelligent MCQ creation
- **Feedback Analysis**: Personalized learning insights
- **Content Processing**: Multi-format content understanding

---

## 🎨 Frontend Options

### Web Interface

- Modern, responsive design
- Interactive dashboard
- Real-time feedback
- Mobile-friendly

### Streamlit Interface

- Python-based UI
- Quick prototyping
- Data science friendly
- Simple deployment

**Choose either frontend based on your preference - both offer full functionality!**

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Open Pull Request

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
