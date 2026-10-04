import logging
import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.analyzer import analyze_job_description


# ============================================================
# LOGGING
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(
    "AIJobAnalyzer"
)


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="AI Job Description Analyzer",
    description=(
        "AI-powered job description analysis "
        "and career roadmap generator."
    ),
    version="1.0.0"
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "frontend"
)


# ============================================================
# STATIC FILES
# ============================================================

app.mount(
    "/static",
    StaticFiles(
        directory=FRONTEND_DIR
    ),
    name="static"
)


# ============================================================
# REQUEST MODEL
# ============================================================

class JobRequest(BaseModel):

    job_description: str = Field(
        ...,
        min_length=30,
        max_length=30000
    )


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():
    return FileResponse(
        os.path.join(
            FRONTEND_DIR,
            "index.html"
        )
    )


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "AI Job Description Analyzer",
        "version": "1.0.0"
    }


# ============================================================
# MODEL
# ============================================================

@app.get("/model")
def model():
    return {
        "provider": "Groq",
        "model": os.getenv(
            "GROQ_MODEL",
            "openai/gpt-oss-20b"
        )
    }


# ============================================================
# ANALYZE
# ============================================================

@app.post("/analyze")
def analyze(request: JobRequest):

    job_description = (
        request.job_description.strip()
    )

    if len(job_description) < 30:
        return {
            "success": False,
            "error": (
                "Please provide a longer "
                "job description."
            )
        }

    logger.info(
        "Analyzing job description "
        "(%s characters)",
        len(job_description)
    )

    try:

        result = analyze_job_description(
            job_description
        )

        return {
            "success": True,
            "analysis": result
        }

    except RuntimeError as error:

        logger.exception(
            "AI analysis failed"
        )

        return {
            "success": False,
            "error": str(error)
        }

    except Exception as error:

        logger.exception(
            "Unexpected analysis error"
        )

        return {
            "success": False,
            "error": (
                "An unexpected server error "
                "occurred."
            )
        }