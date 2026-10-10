import hashlib
import os
import re
from typing import Dict, List, Optional
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr

app = FastAPI(
    title="J Srujan Vishwakarma - AI Engineer Portfolio",
    description="Portfolio website and interactive API showcasing Generative AI, RAG, and MLOps projects.",
    version="1.0.0"
)

static_dir = os.path.join(os.path.dirname(__file__), "static")


class VersionedStaticFiles(StaticFiles):
    """Static files with sane caching.

    URLs built by static_url() carry a content fingerprint (?v=...), so they can be cached for a year: any
    change to a file produces a new URL. Anything requested without a fingerprint is always revalidated, so a
    browser can never keep serving an old stylesheet or script next to new HTML.
    """

    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        if response.status_code in (200, 206, 304):
            fingerprinted = b"v=" in scope.get("query_string", b"")
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable" if fingerprinted else "no-cache"
        return response


# Mount static directory if it exists
if os.path.exists(static_dir):
    app.mount("/static", VersionedStaticFiles(directory=static_dir), name="static")

# Setup Jinja2 templates directory
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

_asset_versions = {}


def static_url(path: str) -> str:
    """URL for a file under /static with a content fingerprint, e.g. /static/css/style.css?v=3fa9c1d2e0."""
    full = os.path.join(static_dir, path)
    try:
        mtime = os.path.getmtime(full)
        cached = _asset_versions.get(path)
        if not cached or cached[0] != mtime:
            with open(full, "rb") as fh:
                cached = (mtime, hashlib.sha256(fh.read()).hexdigest()[:10])
            _asset_versions[path] = cached
        return f"/static/{path}?v={cached[1]}"
    except OSError:
        return f"/static/{path}"


templates.env.globals["static_url"] = static_url


@app.middleware("http")
async def revalidate_pages(request: Request, call_next):
    """HTML and JSON are always revalidated so visitors never see a stale page."""
    response = await call_next(request)
    if response.headers.get("content-type", "").startswith(("text/html", "application/json")):
        response.headers.setdefault("Cache-Control", "no-cache")
    return response

# ==========================================
# RESUME & PORTFOLIO DATA (CENTRAL TRUTH)
# ==========================================
PROFILE_DATA = {
    "name": "J Srujan Vishwakarma",
    "title": "AI Engineer",
    "specialization": "Generative AI | LLMs | RAG | Agentic AI | MCP | VLM Fine-Tuning",
    "email": "srujansrutha01@gmail.com",
    "phone": "+91-9741021059",
    "location": "Bengaluru, India",
    "social": {
        "linkedin": "https://linkedin.com/in/srujan-vishwakarma",
        "github": "https://github.com/srujansrutha",
        "youtube": "https://youtube.com/@SruthasSnap"
    },
    "summary": (
        "AI Engineer with 1+ year building and deploying production LLM and Generative AI systems: RAG pipelines, multi-agent "
        "workflows, MCP integrations, and fine-tuned vision-language models. Fine-tuned Qwen3-VL with QLoRA to 98% accuracy on a "
        "held-out evaluation set and shipped an MCP-powered LLM analytics agent for business stakeholders. Works directly with "
        "brand clients and communicates AI results to non-technical teams."
    ),
    "stats": [
        {"label": "B.E. CGPA", "value": "9.03", "suffix": "/10"},
        {"label": "VLM Labeling Accuracy", "value": "98", "suffix": "%"},
        {"label": "Cloud Cost Optimization", "value": "20", "suffix": "%"},
        {"label": "YouTube Community", "value": "3K", "suffix": "+"}
    ],
    "skills": {
        "languages": ["Python", "SQL"],
        "ai_ml": [
            "PyTorch", "TensorFlow", "scikit-learn", "Hugging Face", "LangChain",
            "LangGraph", "CrewAI", "Pandas", "NumPy", "NLP", "Computer Vision"
        ],
        "generative_ai": [
            "LLMs", "RAG (Retrieval-Augmented Generation)", "Embeddings", "Vector Search",
            "Agentic AI", "Multi-Agent Systems", "MCP (Model Context Protocol)",
            "LLM & VLM Fine-Tuning (LoRA, QLoRA)", "Prompt Engineering", "LLM Evaluation",
            "Guardrails", "OpenAI API"
        ],
        "cloud_mlops": [
            "AWS (Bedrock, SageMaker, EC2, S3)", "GCP", "Docker", "CI/CD (GitHub Actions)",
            "Apache Airflow", "FastAPI (REST APIs)", "Microservices"
        ],
        "databases": [
            "ClickHouse", "MongoDB", "MySQL", "Pinecone", "Qdrant", "Redis"
        ],
        "tools": [
            "Ollama", "N8N", "ComfyUI", "Git", "Web Scraping", "Rapid Prototyping"
        ]
    },
    "experience": [
        {
            "company": "TrendGully",
            "location": "Bangalore",
            "role": "Junior AI Engineer",
            "period": "Jul 2025 – Present",
            "is_current": True,
            "highlights": [
                "Fine-tuned a vision-language model (Qwen3-VL) with QLoRA on ~340K products (1M+ images) for apparel and footwear attribute classification, reaching 98% accuracy on a held-out evaluation set, and integrated it into the ETL labeling workflow.",
                "Built and deployed an MCP-powered LLM analytics agent, integrating the fashion-analytics data layer through an MCP server so business stakeholders can query datasets in natural language.",
                "Migrated data workflows from MongoDB to ClickHouse, cutting analytical query time from ~6-7 s to ~1-2 s.",
                "Automated large-scale web scraping and ETL pipelines covering 230 brands (130 apparel, 70 footwear, 30 marketplace) across structured and unstructured data."
            ],
            "tech_tags": ["Qwen3-VL", "QLoRA", "ClickHouse", "MCP", "ETL", "Web Scraping", "Python"]
        },
        {
            "company": "Ellucian",
            "location": "Bangalore",
            "role": "Cloud Intern",
            "period": "Jan 2025 – Apr 2025",
            "is_current": False,
            "highlights": [
                "Built an AI-driven cloud cost optimization dashboard on AWS SageMaker with predictive analytics, reducing costs by 20% and improving utilization by 15%.",
                "Designed a multi-agent recommendation system integrating multiple AWS services for resource optimization.",
                "Fine-tuned an LLM-based code generation system that converts natural-language prompts into executable code."
            ],
            "tech_tags": ["AWS SageMaker", "Multi-Agent Systems", "LLM Fine-Tuning", "Predictive Analytics"]
        },
        {
            "company": "CSIR4PI (NAL)",
            "location": "Bangalore",
            "role": "AI & Data Science Intern",
            "period": "Sep 2024 – Dec 2024",
            "is_current": False,
            "highlights": [
                "Built a machine learning rainfall forecasting model on 10+ years of CHIRPS climate data for climate-pattern analysis.",
                "Developed preprocessing pipelines for large-scale environmental and geospatial datasets."
            ],
            "tech_tags": ["Climate Data", "Data Science", "Python", "Predictive Modeling", "Geospatial Data"]
        }
    ],
    "education": {
        "institution": "CMR Institute of Technology",
        "location": "Bangalore",
        "degree": "B.E. Artificial Intelligence & Data Science",
        "period": "2021 – 2025",
        "cgpa": "9.03"
    },
    "projects": [
        {
            "id": "agentic-rag",
            "title": "Agentic ChatBot",
            "category": "GenAI & RAG",
            "period": "GitHub",
            "tagline": "LangGraph agent with ClickHouse/MongoDB tools, document + image RAG, memory and guardrails",
            "description": (
                "A LangGraph agent on FastAPI that queries ClickHouse and MongoDB tools to give business-friendly answers, "
                "with RAG over PDF/DOCX and multimodal image RAG using CLIP."
            ),
            "tech_stack": ["FastAPI", "LangGraph", "LangChain", "Ollama", "Redis", "MongoDB", "ClickHouse", "CLIP", "Docker"],
            "features": [
                "Built a LangGraph agent on FastAPI that queries ClickHouse and MongoDB tools for business-friendly answers.",
                "Implemented RAG over PDF/DOCX with sentence-transformer embeddings, plus multimodal image RAG using CLIP.",
                "Added short- and long-term memory via Redis conversation history and LangGraph SQLite checkpointing.",
                "Added guardrails, token-based security, automated tests, an evaluation script, and Docker Compose deployment."
            ],
            "github": "https://github.com/srujansrutha/Agentic-Bot",
            "demo": "#",
            "badge": "Featured"
        },
        {
            "id": "wheat-detection",
            "title": "Global Wheat Detection",
            "category": "Computer Vision & LLM",
            "period": "Intel AI for Youth",
            "tagline": "YOLO11 wheat detection with held-out-farm evaluation and a LoRA-tuned Qwen2.5 advisory model",
            "description": (
                "Fine-tuned YOLO11s on 148K annotations (3.4K images, 7 farms) and evaluated it on held-out farms, paired with a "
                "LoRA fine-tuned Qwen2.5-3B-Instruct that gives crop-quality and fertilizer advice."
            ),
            "tech_stack": ["YOLO11", "PyTorch", "Ultralytics", "Qwen2.5", "LoRA/PEFT", "FastAPI"],
            "features": [
                "Reached 0.945 mAP@50 in-domain and 0.890 on held-out farms.",
                "Built a source-disjoint train/val/OOD split, tracing a 0.15 mAP@50-95 domain-shift gap to object scale and density.",
                "LoRA fine-tuned Qwen2.5-3B-Instruct for crop-quality and fertilizer advice, served via a FastAPI inference endpoint."
            ],
            "github": "https://github.com/srujansrutha/GWD-workflow",
            "demo": "#",
            "badge": "Computer Vision"
        },
        {
            "id": "mcp-fashion-analytics",
            "title": "MCP Fashion Analytics",
            "category": "GenAI & MLOps",
            "period": "TrendGully",
            "tagline": "Natural-language querying of fashion analytics data through an MCP server",
            "description": (
                "An MCP-powered LLM analytics agent that integrates the fashion-analytics data layer through an MCP server, "
                "so business stakeholders can query datasets in natural language."
            ),
            "tech_stack": ["MCP", "ClickHouse", "MongoDB", "Python", "Qwen3-VL"],
            "features": [
                "Integrated the fashion-analytics data layer through an MCP server for LLM context retrieval.",
                "Migrated MongoDB workflows to ClickHouse, cutting analytical query time from ~6-7 s to ~1-2 s.",
                "Fine-tuned Qwen3-VL with QLoRA for attribute labeling: 98% accuracy on a held-out evaluation set."
            ],
            "github": None,
            "demo": "#",
            "badge": "Production AI"
        },
        {
            "id": "cloud-cost-agent",
            "title": "AWS Cloud Cost Optimization Agent",
            "category": "MLOps & Cloud",
            "period": "Ellucian",
            "tagline": "SageMaker predictive analytics and a multi-agent recommender, cutting cloud costs by 20%",
            "description": (
                "An AI-driven cloud cost optimization dashboard on AWS SageMaker with predictive analytics, plus a multi-agent "
                "recommendation system integrating multiple AWS services for resource optimization."
            ),
            "tech_stack": ["AWS SageMaker", "AWS", "Multi-Agent Systems", "Python", "Predictive Analytics"],
            "features": [
                "Reduced cloud costs by 20% and improved utilization by 15% with predictive analytics.",
                "Designed a multi-agent recommendation system integrating multiple AWS services.",
                "Fine-tuned an LLM-based code generation system that converts natural-language prompts into executable code."
            ],
            "github": None,
            "demo": "#",
            "badge": "Enterprise"
        }
    ],
    "achievements_and_certifications": [
        {"title": "AWS Fundamentals Specialization", "issuer": "Coursera", "icon": "aws"},
        {"title": "Agentic AI Certification", "issuer": "DeepLearning.AI", "icon": "brain"},
        {"title": "Winner - Ellucian Hackathon", "issuer": "Ellucian", "icon": "trophy"},
        {"title": "President - JJC Organization (Kotturu Branch)", "issuer": "Leadership", "icon": "users"},
        {"title": "YouTube Creator - 'SruthasSnap'", "issuer": "3K+ Subscribers", "icon": "video"}
    ]
}

# ==========================================
# MLOPS SHOWCASE (served at /mlops and /api/mlops)
# Every claim here comes from the resume or from the public repos linked below
# (srujansrutha/GWD-workflow: .github/workflows/ci.yml, docker/, compose*.yaml, README; srujansrutha/Agentic-Bot).
# ==========================================
MLOPS_DATA = {
    "meta_description": (
        "MLOps projects by J Srujan Vishwakarma: VLM fine-tuning pipelines, a ClickHouse data platform, an MCP analytics agent, "
        "SageMaker cost optimization, plus CI/CD and Docker-based deployment, mapped across the ML lifecycle."
    ),
    "eyebrow": "MLOps · Production ML",
    "headline": "Models in production,",
    "headline_accent": "not just notebooks.",
    "summary": (
        "Data pipelines, fine-tuning, evaluation, deployment and cloud cost control: the full ML lifecycle, "
        "shipped at TrendGully and Ellucian and in my own open-source projects."
    ),
    "stages": [
        {"id": "data", "label": "Data", "blurb": "Scraping, ETL and a fast analytics store."},
        {"id": "train", "label": "Train", "blurb": "LoRA / QLoRA fine-tuning of VLMs, LLMs and detectors."},
        {"id": "evaluate", "label": "Evaluate", "blurb": "Held-out and unseen-domain splits, eval scripts, tests."},
        {"id": "deploy", "label": "Deploy", "blurb": "Docker, FastAPI, MCP servers, CI on GitHub Actions."},
        {"id": "operate", "label": "Operate", "blurb": "Guardrails, memory and cloud cost control on AWS."},
    ],
    "pipeline_log": [
        {"stage": "data", "text": "230 brands · ETL · MongoDB → ClickHouse", "state": "ok"},
        {"stage": "train", "text": "Qwen3-VL · QLoRA · ~340K products, 1M+ images", "state": "ok"},
        {"stage": "evaluate", "text": "98% on a held-out set · unseen-farm splits", "state": "ok"},
        {"stage": "deploy", "text": "Docker Compose · FastAPI · MCP · CI/CD", "state": "ok"},
        {"stage": "operate", "text": "SageMaker · cost -20% · utilization +15%", "state": "run"},
    ],
    "stats": [
        {"value": "98", "suffix": "%", "label": "VLM accuracy on a held-out set", "count": True},
        {"value": "230", "suffix": "", "label": "brands in scraping + ETL pipelines", "count": True},
        {"value": "1–2", "suffix": "s", "label": "analytics queries, down from ~6–7 s", "count": False},
        {"value": "20", "suffix": "%", "label": "cloud cost cut on AWS (utilization +15%)", "count": True},
    ],
    "projects": [
        {
            "id": "wheat-advisor-ci",
            "featured": True,
            "title": "Wheat Advisor: CI, containers and honest evaluation",
            "kicker": "FLAGSHIP · OPEN SOURCE",
            "org": "GitHub · Intel AI for Youth",
            "stages": ["train", "evaluate", "deploy"],
            "summary": (
                "A YOLO11 wheat-head detector plus a LangGraph field-report workflow, packaged so anyone can run it: "
                "every push is linted, tested and built into a Docker image that has to pass a live health check."
            ),
            "bullets": [
                "GitHub Actions on every push: ruff lint, pytest, Docker image build and a live health check.",
                "116 automated tests that need no GPU, network or language model.",
                "Docker Compose runs the app and a local LLM as separate containers, with a CPU/GPU overlay; weights are mounted, not baked into the image.",
                "Farm-level held-out evaluation: adding diverse farms doubled the unseen-farm score (0.149 → 0.301 mAP@50-95) with the same small model.",
            ],
            "ci_steps": [
                "ruff lint",
                "pytest · 116 tests",
                "compose config · CPU + GPU",
                "build app image",
                "start app + health check",
                "import smoke test",
            ],
            "stack": ["YOLO11", "LangGraph", "Docker Compose", "GitHub Actions", "pytest", "Ollama"],
            "github": "https://github.com/srujansrutha/GWD-workflow",
            "ci_url": "https://github.com/srujansrutha/GWD-workflow/actions/workflows/ci.yml",
        },
        {
            "id": "agentic-chatbot-ops",
            "featured": False,
            "title": "Agentic ChatBot: guardrails, tests and containers",
            "kicker": "OPEN SOURCE",
            "org": "GitHub",
            "stages": ["evaluate", "deploy", "operate"],
            "summary": (
                "A LangGraph agent on FastAPI that queries ClickHouse and MongoDB tools, built to be operated: "
                "guarded, tested, evaluated and containerised."
            ),
            "bullets": [
                "Guardrails and token-based security in front of the agent.",
                "Automated tests plus an evaluation script.",
                "Redis conversation history and LangGraph SQLite checkpointing for short- and long-term memory.",
                "Dockerfile and Docker Compose deployment.",
            ],
            "stack": ["FastAPI", "LangGraph", "Docker Compose", "Redis", "ClickHouse", "MongoDB"],
            "github": "https://github.com/srujansrutha/Agentic-Bot",
        },
        {
            "id": "vlm-labeling-pipeline",
            "featured": False,
            "title": "VLM attribute-labeling pipeline",
            "kicker": "PRODUCTION",
            "org": "TrendGully",
            "stages": ["train", "evaluate", "deploy"],
            "summary": "Fine-tuned Qwen3-VL with QLoRA to label apparel and footwear attributes, then wired it into production ETL.",
            "bullets": [
                "98% accuracy on a held-out evaluation set.",
                "Trained on ~340K products (1M+ images).",
                "Integrated into the ETL labeling workflow.",
            ],
            "stack": ["Qwen3-VL", "QLoRA", "ETL"],
            "github": None,
        },
        {
            "id": "fashion-data-platform",
            "featured": False,
            "title": "Fashion data platform: ETL and ClickHouse",
            "kicker": "PRODUCTION",
            "org": "TrendGully",
            "stages": ["data"],
            "summary": "Automated scraping and ETL for 230 brands and moved analytical workloads from MongoDB to ClickHouse.",
            "bullets": [
                "Analytical queries cut from ~6–7 s to ~1–2 s.",
                "230 brands: 130 apparel, 70 footwear, 30 marketplace.",
                "Structured and unstructured data handled in the same pipelines.",
            ],
            "stack": ["ClickHouse", "MongoDB", "ETL", "Web Scraping", "Python"],
            "github": None,
        },
        {
            "id": "mcp-analytics-agent",
            "featured": False,
            "title": "MCP analytics agent",
            "kicker": "PRODUCTION",
            "org": "TrendGully",
            "stages": ["deploy", "operate"],
            "summary": (
                "An MCP server exposes the fashion-analytics data layer to an LLM agent, "
                "so business stakeholders can query datasets in natural language."
            ),
            "bullets": [
                "Built and deployed for business stakeholders.",
                "Fashion-analytics data layer integrated through an MCP server.",
            ],
            "stack": ["MCP", "LLM agent"],
            "github": None,
        },
        {
            "id": "cloud-cost-optimization",
            "featured": False,
            "title": "Cloud cost optimization on SageMaker",
            "kicker": "ENTERPRISE · INTERNSHIP",
            "org": "Ellucian",
            "stages": ["operate"],
            "summary": (
                "An AI-driven cost optimization dashboard on AWS SageMaker with predictive analytics, "
                "plus a multi-agent recommender spanning several AWS services."
            ),
            "bullets": [
                "Cloud costs down 20%.",
                "Resource utilization up 15%.",
                "Multi-agent recommendation system integrating multiple AWS services.",
            ],
            "stack": ["AWS SageMaker", "Multi-Agent", "Predictive Analytics"],
            "github": None,
            "wide": True,
            "metrics": [
                {"value": "−20%", "label": "cloud cost"},
                {"value": "+15%", "label": "resource utilization"},
            ],
        },
    ],
    "toolkit": [
        {"group": "SHIP", "items": ["Docker", "Docker Compose", "CI/CD (GitHub Actions)", "Git", "FastAPI (REST APIs)", "Microservices"]},
        {"group": "ORCHESTRATE", "items": ["Apache Airflow", "N8N", "MCP servers"]},
        {"group": "CLOUD", "items": ["AWS SageMaker", "AWS Bedrock", "EC2", "S3", "GCP"]},
        {"group": "DATA", "items": ["ClickHouse", "MongoDB", "MySQL", "Redis", "Qdrant", "Pinecone"]},
        {"group": "QUALITY", "items": ["LLM Evaluation", "Guardrails", "Automated tests", "Held-out / OOD splits"]},
        {"group": "MODELS", "items": ["LoRA / QLoRA", "Hugging Face", "PyTorch", "Ollama"]},
    ],
}
for _stage in MLOPS_DATA["stages"]:
    _stage["count"] = sum(1 for _p in MLOPS_DATA["projects"] if _stage["id"] in _p["stages"])

try:
    from pydantic import EmailStr
except ImportError:
    EmailStr = str  # Fallback to standard string if email-validator is not installed

# Pydantic Schemas
class ContactMessage(BaseModel):
    name: str
    email: EmailStr
    subject: Optional[str] = "Portfolio Contact Form Inquiry"
    message: str

class ChatQuery(BaseModel):
    message: str

# ==========================================
# ROUTES
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serves the main interactive portfolio page."""
    return templates.TemplateResponse(request=request, name="index.html", context={"profile": PROFILE_DATA})

@app.get("/mlops", response_class=HTMLResponse)
async def read_mlops(request: Request):
    """Serves the MLOps projects page."""
    return templates.TemplateResponse(request=request, name="mlops.html", context={"profile": PROFILE_DATA, "mlops": MLOPS_DATA})

@app.get("/api/profile")
async def get_profile_json():
    """Returns complete raw JSON profile data."""
    return JSONResponse(content=PROFILE_DATA)

@app.get("/api/mlops")
async def get_mlops_json():
    """Returns the MLOps showcase data (stages, stats, projects, toolkit)."""
    return JSONResponse(content=MLOPS_DATA)

@app.get("/api/projects")
async def get_projects(category: Optional[str] = None):
    """Returns projects list, optionally filtered by category."""
    projects = PROFILE_DATA["projects"]
    if category and category.lower() != "all":
        projects = [p for p in projects if category.lower() in p["category"].lower()]
    return JSONResponse(content=projects)

@app.get("/api/experience")
async def get_experience():
    """Returns work history data."""
    return JSONResponse(content=PROFILE_DATA["experience"])

@app.get("/api/skills")
async def get_skills():
    """Returns skills matrix."""
    return JSONResponse(content=PROFILE_DATA["skills"])

@app.post("/api/contact")
async def handle_contact(contact: ContactMessage):
    """Handles contact form submissions."""
    # In production, message can be sent via SendGrid, Email API, or saved to DB
    return {
        "status": "success",
        "message": f"Thank you, {contact.name}! Srujan has received your message and will reply shortly to {contact.email}."
    }

def _keyword_reply(msg: str) -> str:
    """Fallback keyword responder used when no LLM API key is configured."""
    if any(k in msg for k in ["mlops", "ci/cd", "devops", "production ml"]):
        reply = (
            "Srujan's MLOps work spans the whole ML lifecycle: scraping + ETL for 230 brands and a MongoDB to ClickHouse migration "
            "(queries ~6-7 s to ~1-2 s), Qwen3-VL QLoRA fine-tuning at 98% held-out accuracy, an MCP analytics agent in production, "
            "AWS SageMaker cost optimization (-20% cost), and open-source repos with GitHub Actions CI, Docker Compose and automated tests. "
            "See the full breakdown at /mlops."
        )
    elif any(k in msg for k in ["hello", "hi", "hey", "who are you"]):
        reply = (
            "Greetings! I am Srujan's Portfolio AI Assistant. "
            "Srujan is an AI Engineer specializing in Generative AI, LLMs, RAG, Agentic AI, MCP, and VLM fine-tuning. "
            "Feel free to ask me about his work at TrendGully, Ellucian, projects like the Agentic ChatBot, or his skills!"
        )
    elif any(k in msg for k in ["rag", "agentic", "langgraph", "vector"]):
        reply = (
            "Srujan built an Agentic ChatBot: a LangGraph agent on FastAPI that queries ClickHouse and MongoDB tools, "
            "with RAG over PDF/DOCX, multimodal image RAG using CLIP, Redis + SQLite-checkpointed memory, "
            "guardrails, automated tests and Docker Compose deployment."
        )
    elif any(k in msg for k in ["vlm", "vision", "fashion", "trendgully", "accuracy"]):
        reply = (
            "At TrendGully (Junior AI Engineer), Srujan fine-tuned Qwen3-VL with QLoRA on ~340K products (1M+ images) for apparel "
            "and footwear attribute classification, reaching 98% accuracy on a held-out set. He also migrated analytics from MongoDB "
            "to ClickHouse (~6-7 s to ~1-2 s queries) and built an MCP-powered LLM analytics agent."
        )
    elif any(k in msg for k in ["ellucian", "aws", "cost", "cloud", "sagemaker"]):
        reply = (
            "During his Cloud Internship at Ellucian, Srujan built an AI-driven AWS infrastructure cost optimization dashboard "
            "using SageMaker & Multi-Agent systems, successfully cutting cloud costs by 20% and boosting utilization efficiency by 15%."
        )
    elif any(k in msg for k in ["wheat", "yolo", "intel", "hackathon"]):
        reply = (
            "Srujan built 'Global Wheat Detection' (Intel AI for Youth). He fine-tuned YOLO11s to 0.945 mAP@50 in-domain and 0.890 "
            "on held-out farms, and LoRA fine-tuned Qwen2.5-3B-Instruct for crop-quality and fertilizer advice, served via FastAPI."
        )
    elif any(k in msg for k in ["skills", "python", "tech stack", "tools"]):
        reply = (
            "Srujan's tech stack includes:\n"
            "• Languages: Python, SQL\n"
            "• AI/ML: PyTorch, TensorFlow, Hugging Face, LangChain, LangGraph, CrewAI, FastAPI\n"
            "• GenAI: RAG, Agentic AI, Multi-Agent Systems, LoRA/QLoRA fine-tuning, Vector Search, MCP\n"
            "• Databases & MLOps: ClickHouse, Qdrant, Redis, MongoDB, AWS (SageMaker, Bedrock), Docker, GitHub Actions"
        )
    elif any(k in msg for k in ["cgpa", "college", "education", "cmr"]):
        reply = (
            "Srujan graduated with a B.E. in Artificial Intelligence & Data Science from CMR Institute of Technology, Bangalore (2021-2025) "
            "achieving a stellar CGPA of 9.03 / 10!"
        )
    elif any(k in msg for k in ["contact", "email", "phone", "hire"]):
        reply = (
            f"You can connect directly with Srujan via:\n"
            f"• Email: {PROFILE_DATA['email']}\n"
            f"• Phone: {PROFILE_DATA['phone']}\n"
            f"• Location: {PROFILE_DATA['location']}\n"
            "Or submit a message using the Contact section below!"
        )
    else:
        reply = (
            f"Srujan Vishwakarma is an AI Engineer in Bangalore with 1+ year building production Generative AI, RAG, and agentic systems. "
            f"He has worked at TrendGully and Ellucian, built high-performance projects, and holds a 9.03 CGPA. "
            f"Try asking specifically about his 'RAG project', 'AWS experience', 'VLM work', or 'Skills'!"
        )

    return reply


@app.post("/api/chat")
async def ai_chat_assistant(query: ChatQuery):
    """LLM-backed assistant (Anthropic) grounded in PROFILE_DATA, with keyword fallback."""
    user_msg = query.message.strip()
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if api_key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            system = (
                f"You are the AI assistant (COMMS) for {PROFILE_DATA['name']}'s portfolio, "
                f"a {PROFILE_DATA['title']} based in {PROFILE_DATA['location']}. Answer visitor and "
                f"recruiter questions about him warmly and concisely (2-4 sentences), in third person. "
                f"Summary: {PROFILE_DATA['summary']} Specialization: {PROFILE_DATA['specialization']}. "
                f"Education: {PROFILE_DATA['education']['degree']} at {PROFILE_DATA['education']['institution']} "
                f"({PROFILE_DATA['education']['period']}), CGPA {PROFILE_DATA['education']['cgpa']}. "
                f"Contact: {PROFILE_DATA['email']}, {PROFILE_DATA['phone']}. Experience: "
                + " | ".join(f"{e['company']} - {e['role']} ({e['period']})" for e in PROFILE_DATA['experience'])
                + ". Projects: "
                + " | ".join(f"{p['title']}: {p['tagline']}" for p in PROFILE_DATA['projects'])
                + ". MLOps projects (full page at /mlops): "
                + " | ".join(f"{p['title']} ({p['org']}; stages: {', '.join(p['stages'])})" for p in MLOPS_DATA['projects'])
                + ". If asked something unrelated to Srujan, gently redirect to his work. Never invent facts beyond these."
            )
            resp = client.messages.create(
                model=os.environ.get("CHAT_MODEL", "claude-3-5-haiku-latest"),
                max_tokens=400,
                system=system,
                messages=[{"role": "user", "content": user_msg}],
            )
            text = "".join(getattr(b, "text", "") for b in resp.content).strip()
            if text:
                return {"response": text}
        except Exception as e:
            print("LLM chat failed, using keyword fallback:", e)
    return {"response": _keyword_reply(user_msg.lower())}


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting Srujan's AI Portfolio Server on port {port}...")
    uvicorn.run("profile:app", host="0.0.0.0", port=port, reload=True)
