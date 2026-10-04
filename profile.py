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

# Mount static directory if it exists
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Setup Jinja2 templates directory
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

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

@app.get("/api/profile")
async def get_profile_json():
    """Returns complete raw JSON profile data."""
    return JSONResponse(content=PROFILE_DATA)

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
    if any(k in msg for k in ["hello", "hi", "hey", "who are you"]):
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
