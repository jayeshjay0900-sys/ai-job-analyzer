import json
import os

import requests
from dotenv import load_dotenv


load_dotenv()


GROQ_URL = os.getenv(
    "GROQ_URL",
    "https://api.groq.com/openai/v1/chat/completions"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b"
)


def build_prompt(job_description: str) -> str:

    return f"""
You are a professional AI job-description analyzer.

Analyze the job description below.

Return ONLY one valid JSON object.

Do NOT use Markdown.
Do NOT use ```json.
Do NOT add explanations before or after the JSON.

The JSON must contain exactly these fields:

job_title
summary
experience
education
technical_skills
soft_skills
tools_and_technologies
important_keywords
priority_skills
learning_roadmap
project_ideas

Rules:

- job_title must be a string.
- summary must be a string.
- All other fields must be JSON arrays of strings.
- Do not invent requirements.
- Only use information supported by the job description.
- Keep the answers concise.
- learning_roadmap should contain practical learning steps.
- project_ideas should contain practical portfolio projects.

Example format:

{{
  "job_title": "Junior AI Engineer",
  "summary": "Short summary",
  "experience": [
    "Python programming",
    "Machine learning"
  ],
  "education": [
    "Bachelor's degree in Computer Science"
  ],
  "technical_skills": [
    "Python",
    "Machine Learning"
  ],
  "soft_skills": [
    "Communication"
  ],
  "tools_and_technologies": [
    "FastAPI",
    "SQL",
    "Git"
  ],
  "important_keywords": [
    "AI Engineer",
    "Python",
    "Machine Learning"
  ],
  "priority_skills": [
    "Python",
    "Machine Learning"
  ],
  "learning_roadmap": [
    "Master Python",
    "Learn machine learning"
  ],
  "project_ideas": [
    "Build a machine learning REST API"
  ]
}}

JOB DESCRIPTION:

{job_description}
"""


def extract_json(text: str):

    text = text.strip()

    # Remove markdown fences if the model adds them
    text = text.replace(
        "```json",
        ""
    )

    text = text.replace(
        "```",
        ""
    )

    text = text.strip()

    # Try direct JSON
    try:

        return json.loads(text)

    except json.JSONDecodeError:

        pass

    # Find first { and last }
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1:

        json_text = text[
            start:end + 1
        ]

        try:

            return json.loads(
                json_text
            )

        except json.JSONDecodeError:

            pass

    raise RuntimeError(
        "AI returned invalid JSON."
    )


def analyze_job_description(
    job_description: str
):

    api_key = os.getenv(
        "GROQ_API_KEY",
        ""
    ).strip()

    if not api_key:

        raise RuntimeError(
            "GROQ_API_KEY is not configured."
        )

    prompt = build_prompt(
        job_description
    )

    payload = {

        "model": GROQ_MODEL,

        "messages": [

            {
                "role": "system",
                "content": (
                    "You analyze job descriptions. "
                    "Return only valid JSON."
                )
            },

            {
                "role": "user",
                "content": prompt
            }

        ],

        "temperature": 0.1,

        "max_tokens": 1500
    }

    headers = {

        "Authorization":
            f"Bearer {api_key}",

        "Content-Type":
            "application/json"
    }

    try:

        response = requests.post(

            GROQ_URL,

            headers=headers,

            json=payload,

            timeout=60
        )

        response.raise_for_status()

    except requests.exceptions.Timeout as error:

        raise RuntimeError(
            "AI request timed out."
        ) from error

    except requests.exceptions.ConnectionError as error:

        raise RuntimeError(
            "Could not connect to the AI service."
        ) from error

    except requests.exceptions.HTTPError as error:

        try:

            error_details = (
                response.json()
            )

        except ValueError:

            error_details = response.text

        raise RuntimeError(
            f"AI service returned HTTP "
            f"{response.status_code}: "
            f"{error_details}"
        ) from error

    except requests.exceptions.RequestException as error:

        raise RuntimeError(
            f"AI request failed: {error}"
        ) from error

    try:

        data = response.json()

    except ValueError as error:

        raise RuntimeError(
            "AI service returned invalid JSON."
        ) from error

    try:

        content = (
            data["choices"][0]
            ["message"]["content"]
        )

    except (
        KeyError,
        IndexError,
        TypeError
    ) as error:

        raise RuntimeError(
            "AI service returned an unexpected response."
        ) from error

    result = extract_json(
        content
    )

    if not isinstance(
        result,
        dict
    ):

        raise RuntimeError(
            "AI returned an invalid analysis."
        )

    required_fields = [

        "job_title",
        "summary",
        "experience",
        "education",
        "technical_skills",
        "soft_skills",
        "tools_and_technologies",
        "important_keywords",
        "priority_skills",
        "learning_roadmap",
        "project_ideas"

    ]

    for field in required_fields:

        if field not in result:

            if field in [
                "job_title",
                "summary"
            ]:

                result[field] = ""

            else:

                result[field] = []

    return result