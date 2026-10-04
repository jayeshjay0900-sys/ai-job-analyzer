# AI Job Description Analyzer

An AI-powered web application that analyzes job descriptions and converts them into practical career insights, including required skills, priorities, learning roadmaps, and portfolio project ideas.

## 🚀 Live Demo

**[Open the AI Job Description Analyzer](https://aianalyze.onrender.com)**

---

## ✨ Features

* 🤖 AI-powered job description analysis
* 📋 Automatic job title detection
* 🧠 Technical skill extraction
* 🤝 Soft skill extraction
* 🛠️ Tools and technologies identification
* 🎯 Priority skill identification
* 🔑 Important keyword extraction
* 🎓 Education requirement analysis
* 💼 Experience requirement analysis
* 📚 Personalized learning roadmap
* 💡 Portfolio project recommendations
* 📱 Responsive web interface
* ⚡ Lightweight architecture designed for cloud deployment
* 🔐 Secure API-key handling through environment variables

---

## 🏗️ Architecture

```text
                 ┌─────────────────────┐
                 │       Browser       │
                 │   HTML/CSS/JavaScript│
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │       FastAPI       │
                 │      Backend        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │       Groq API      │
                 │     AI Analysis     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Structured JSON   │
                 │      Analysis       │
                 └─────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* Pydantic
* Uvicorn
* Requests

### AI

* Groq API
* `openai/gpt-oss-20b`

### Frontend

* HTML5
* CSS3
* JavaScript

### Deployment

* GitHub
* Render

### Testing

* Pytest
* FastAPI TestClient

---

## 📂 Project Structure

```text
ai-job-analyzer/
│
├── app/
│   ├── __init__.py
│   ├── analyzer.py
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── tests/
│   ├── __init__.py
│   └── test_api.py
│
├── .env.example
├── .gitignore
├── README.md
├── render.yaml
└── requirements.txt
```

---

## 🔄 How It Works

1. The user pastes a job description.
2. The frontend sends the description to the FastAPI backend.
3. FastAPI sends the job description to the Groq API.
4. The AI analyzes the job requirements.
5. The response is converted into structured JSON.
6. The frontend displays the analysis in separate sections.

The application extracts:

* Job title
* Summary
* Experience
* Education
* Technical skills
* Soft skills
* Tools and technologies
* Important keywords
* Priority skills
* Learning roadmap
* Portfolio project ideas

---

## 💻 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/jayeshjay0900-sys/ai-job-analyzer.git
```

### 2. Enter the project

```bash
cd ai-job-analyzer
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

#### Windows

```powershell
.venv\Scripts\activate
```

#### macOS / Linux

```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure environment variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
GROQ_URL=https://api.groq.com/openai/v1/chat/completions
```

**Never commit your `.env` file to GitHub.**

### 7. Start the application

```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

---

## 🧪 Run Tests

Run:

```bash
pytest
```

Current test coverage includes:

* Health endpoint
* Homepage
* Input validation
* Model endpoint

---

## ☁️ Deployment

The application is deployed on Render using a lightweight Python web service.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

The Groq API key is configured securely through Render environment variables.

---

## 🔐 Environment Variables

The application uses:

```text
GROQ_API_KEY
GROQ_MODEL
GROQ_URL
```

The API key is never stored directly in the source code.

---

## 📡 API Endpoints

### Health

```text
GET /health
```

Returns the health status of the application.

### Model

```text
GET /model
```

Returns the configured AI provider and model.

### Analyze

```text
POST /analyze
```

Analyzes a submitted job description.

Example request:

```json
{
    "job_description": "Looking for a Python developer with experience in FastAPI and machine learning."
}
```

---

## 🎯 Project Goals

This project was built to demonstrate practical skills in:

* AI application development
* FastAPI backend development
* REST API integration
* Prompt engineering
* Structured AI output handling
* Frontend development
* API security
* Automated testing
* Cloud deployment

---

## ⚠️ Disclaimer

This application provides AI-generated career insights for educational and informational purposes.

It does not guarantee employment, interview selection, or hiring outcomes. Users should independently verify job requirements and make their own career decisions.

---

## 👨‍💻 Author

**Jayana**

AI / ML & Data Science Student

Interested in:

* Artificial Intelligence
* Machine Learning
* NLP
* LLM Applications
* RAG Systems
* Data Science
* AI Engineering

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.
