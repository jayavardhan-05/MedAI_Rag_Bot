# MED AI - Interactive Medical Interface

A clean, professional, and highly interactive web-based user interface for medical document question-answering. MED AI allows medical students, researchers, and professionals to ask questions about a pre-loaded medical knowledge base and receive AI-generated answers along with source text snippets.

![MED AI Interface](https://img.shields.io/badge/Status-Ready-brightgreen) ![Python](https://img.shields.io/badge/Python-3.8+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green) ![LangChain](https://img.shields.io/badge/LangChain-Latest-orange)

## 🏥 Features

### Core Functionality
- **Interactive Chat Interface**: Clean, modern chat UI with real-time responses
- **AI-Powered Answers**: Get intelligent responses to medical questions
- **Source Attribution**: View exact text snippets used to generate answers
- **Conversation History**: Track all questions and answers in the current session
- **Real-time Status**: Live backend connection status indicator

### User Experience
- **Professional Design**: Medical-themed interface with clean aesthetics
- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Loading Indicators**: Visual feedback during AI processing
- **Error Handling**: User-friendly error messages and recovery
- **Keyboard Shortcuts**: Quick navigation and input controls
- **Sample Questions**: Pre-populated examples to get started

### Technical Features
- **RAG Architecture**: Retrieval-Augmented Generation with FAISS vector database
- **FastAPI Backend**: High-performance REST API with automatic documentation
- **Real-time Health Checks**: Automatic backend monitoring
- **CORS Enabled**: Ready for deployment and development

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Medical documents processed into FAISS index (see notebook)
- Google API key for Gemini (optional, fallback mode available)

### 1. Install Dependencies

```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt
```

### 2. Set Up Environment (Optional)

```bash
# For full AI functionality, set your Google API key
export GOOGLE_API_KEY="your-google-api-key-here"
```

### 3. Start the Backend

```bash
# From the backend directory
python run_server.py
```

The startup script will:
- Check for all required dependencies
- Locate and set up the FAISS index
- Start the FastAPI server on `http://localhost:8000`

### 4. Start the Frontend

```bash
# From the frontend directory
cd ../frontend
python serve.py
```

The frontend will be available at `http://localhost:3000` and should open automatically in your browser.

## 📁 Project Structure

```
MED AI/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   ├── run_server.py        # Backend startup script
│   └── my_faiss_index/      # FAISS vector database (auto-copied)
├── frontend/
│   ├── index.html           # Main HTML interface
│   ├── styles.css           # Professional styling
│   ├── script.js            # Interactive functionality
│   └── serve.py             # Frontend server script
├── my_faiss_index/          # Original FAISS database
├── MedAI.ipynb              # Document processing notebook
└── README.md                # This file
```

## 🎯 Usage Guide

### Asking Questions

1. **Type your question** in the input field at the bottom
2. **Press Enter** or click the send button
3. **Watch the AI think** with the animated thinking indicator
4. **Read the answer** in the chat area
5. **Check sources** in the right panel for verification

### Sample Questions

Try these example questions to get started:
- "What are the symptoms of hypertension?"
- "Explain the pathophysiology of diabetes"
- "What are the treatment options for pneumonia?"
- "Describe the causes of myocardial infarction"

### Keyboard Shortcuts

- **Enter**: Send question
- **Ctrl/Cmd + K**: Focus on input field
- **Escape**: Clear input field

### Status Indicators

- 🟢 **Connected**: Backend is running and database is loaded
- 🟡 **Connecting**: Checking backend status
- 🔴 **Error**: Backend issues or offline

## 🔧 API Documentation

The FastAPI backend provides a REST API with automatic documentation:

- **API Base URL**: `http://localhost:8000`
- **Interactive Docs**: `http://localhost:8000/docs`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

### Main Endpoints

#### POST `/ask`
Ask a medical question and get an AI-generated answer with sources.

**Request:**
```json
{
  "question": "What are the symptoms of hypertension?"
}
```

**Response:**
```json
{
  "answer": "Hypertension often presents with...",
  "sources": [
    {
      "content": "Source text content...",
      "metadata": {"source": "document.pdf", "page": 123}
    }
  ]
}
```

#### GET `/health`
Check backend status and database availability.

**Response:**
```json
{
  "database_loaded": true,
  "qa_chain_ready": true,
  "status": "healthy"
}
```

## 🛠️ Configuration

### Backend Configuration

Edit `backend/main.py` to configure:
- **API Base URL**: Update CORS settings for production
- **Model Settings**: Change AI model parameters
- **Retrieval Settings**: Adjust number of source documents

### Frontend Configuration

Edit `frontend/script.js` to configure:
- **API_BASE_URL**: Change backend endpoint
- **UI Settings**: Modify behavior and appearance

## 🔒 Production Deployment

### Security Considerations

1. **CORS Settings**: Update `allow_origins` in `main.py` for production
2. **API Keys**: Use environment variables, never hardcode
3. **HTTPS**: Enable SSL/TLS for production deployment
4. **Rate Limiting**: Consider adding rate limiting for public deployment

### Deployment Options

1. **Docker**: Containerize both frontend and backend
2. **Cloud Platforms**: Deploy to AWS, GCP, or Azure
3. **Static Hosting**: Serve frontend from CDN
4. **Reverse Proxy**: Use nginx for production serving

## 🐛 Troubleshooting

### Common Issues

**"FAISS index not found"**
- Run the Jupyter notebook to create the index
- Ensure `my_faiss_index` folder exists in project root

**"Backend offline" status**
- Check if backend server is running on port 8000
- Verify all dependencies are installed
- Check console for error messages

**"No sources found"**
- Verify FAISS index contains documents
- Check if question matches medical content
- Try rephrasing the question

**CORS errors**
- Ensure frontend is served from a web server (not file://)
- Check CORS settings in backend configuration

### Debug Mode

Enable debug logging in the backend:
```python
# In main.py, change log level
uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **LangChain**: For the RAG framework
- **FastAPI**: For the high-performance backend
- **FAISS**: For efficient vector similarity search
- **Google Gemini**: For AI language model capabilities
- **Inter Font**: For clean typography
- **Font Awesome**: For professional icons

## 📞 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review the API documentation

---

**MED AI** - Empowering medical research with AI-powered question answering 🏥✨