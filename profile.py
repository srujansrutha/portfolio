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
    "specialization": "Generative AI | Multi-Agent RAG | Vision-Language Models | Cloud MLOps",
    "email": "srujansrutha01@gmail.com",
    "phone": "+91-9741021059",
    "location": "Bengaluru, India",
    "social": {
        "linkedin": "https://linkedin.com/in/j-srujan-vishwakarma",
        "github": "https://github.com/srujan-vishwakarma",
        "youtube": "https://youtube.com/@SruthasSnap"
    },
    "summary": (
        "AI Engineer specializing in Generative AI, multi-agent RAG systems, Vision-Language Models, and scalable ML pipelines. "
        "Experienced in ClickHouse migration, MCP-powered conversational analytics, multimodal model fine-tuning, and cloud-native "
        "deployment using AWS, FastAPI, and modern LLM frameworks."
    ),
    "stats": [
        {"label": "B.E. CGPA", "value": "9.03", "suffix": "/10"},
        {"label": "VLM Labeling Accuracy", "value": "98", "suffix": "%"},
        {"label": "Cloud Cost Optimization", "value": "20", "suffix": "%"},
        {"label": "YouTube Community", "value": "3K", "suffix": "+"}
    ],
    "skills": {
        "languages": ["Python", "SQL", "Bash"],
        "ai_ml": [
            "PyTorch", "Transformers", "scikit-learn", "LangChain", 
            "LangGraph", "CrewAI", "Hugging Face", "FastAPI", "OpenCV"
        ],
        "generative_ai": [
            "RAG (Retrieval-Augmented Generation)", "Multi-Agent Systems", 
            "LLM Fine-Tuning", "Prompt Engineering", "Vector Search", 
            "Multimodal AI", "MCP (Model Context Protocol)"
        ],
        "cloud_mlops": [
            "AWS (SageMaker, Bedrock, EC2, S3)", "Docker", 
            "Apache Airflow", "ETL Pipelines", "Model Deployment"
        ],
        "databases": [
            "ClickHouse", "MongoDB", "MySQL", "Pinecone", "Qdrant", "Redis"
        ],
        "tools": [
            "Ollama", "N8N", "ComfyUI", "Git", "Jupyter", "Linux"
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
                "Maintained and optimized large-scale fashion scraping pipelines, migrating workflows from MongoDB to ClickHouse to improve scalability and analytics performance.",
                "Engineered ETL pipelines for structured and unstructured fashion datasets across distributed workflows.",
                "Fine-tuned a Vision-Language Model (VLM) for apparel labeling and attribute classification workflows, achieving 98% accuracy.",
                "Built and deployed an MCP-powered conversational analytics chatbot enabling natural language interaction with fashion datasets."
            ],
            "tech_tags": ["Vision-Language Models", "ClickHouse", "MCP", "ETL", "Python", "FastAPI"]
        },
        {
            "company": "Ellucian",
            "location": "Bangalore",
            "role": "Cloud Intern",
            "period": "Jan 2025 – Apr 2025",
            "is_current": False,
            "highlights": [
                "Built an AI-driven infrastructure cost optimization dashboard using AWS SageMaker, reducing cloud costs by 20%.",
                "Designed a multi-agent recommendation system integrating multiple AWS services for intelligent resource optimization.",
                "Boosted infrastructure utilization efficiency by 15% through predictive analytics workflows.",
                "Fine-tuned an LLM-based code generation system for converting natural language prompts into executable code."
            ],
            "tech_tags": ["AWS SageMaker", "Multi-Agent Systems", "LLM Fine-Tuning", "Predictive Analytics"]
        },
        {
            "company": "CSIR4PI (NAL)",
            "location": "Bangalore",
            "role": "AI Data Science Intern",
            "period": "Sep 2024 – Dec 2024",
            "is_current": False,
            "highlights": [
                "Built a rainfall prediction model using 10+ years of CHIRPS climate datasets for environmental forecasting and climate pattern analysis.",
                "Analyzed 10+ years of climatic data to identify environmental trends and actionable insights.",
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
            "title": "Agentic RAG Application",
            "category": "GenAI & RAG",
            "period": "2024 - 2025",
            "tagline": "Microservices-based multi-agent retrieval platform with LangGraph & Qdrant",
            "description": (
                "Architected an enterprise-grade agentic RAG platform for low-latency contextual retrieval. "
                "Utilizes LangGraph for autonomous retrieval, reasoning, and memory orchestration, coupled with vector search "
                "and async web scraping agents."
            ),
            "tech_stack": ["FastAPI", "LangGraph", "Qdrant", "Redis", "Ollama", "Docker", "LangChain"],
            "features": [
                "Architected a microservices-based RAG platform for low-latency contextual retrieval.",
                "Implemented autonomous workflows using LangGraph for retrieval, reasoning, and memory orchestration.",
                "Integrated Parallel Web Systems with LangChain-based agent workflows for asynchronous multi-source web research.",
                "Designed scalable vector-search infrastructure enabling real-time context-aware responses."
            ],
            "github": "https://github.com/srujan-vishwakarma/agentic-rag",
            "demo": "#",
            "badge": "Featured"
        },
        {
            "id": "wheat-detection",
            "title": "Global Wheat Detection & Crop Analytics",
            "category": "Computer Vision & LLM",
            "period": "Intel AI for Youth Winner",
            "tagline": "Real-time crop detection, quality assessment with fine-tuned LLaMA & advisory system",
            "description": (
                "Real-time computer vision system built for agricultural analytics. Combines YOLO crop object detection "
                "with fine-tuned LLaMA transformers to deliver actionable AI-driven fertilizer and crop-health recommendations."
            ),
            "tech_stack": ["YOLO", "PyTorch", "OpenCV", "Transformers", "LLaMA", "FastAPI"],
            "features": [
                "Built a YOLO-based real-time wheat detection system using OpenCV and PyTorch.",
                "Fine-tuned an LLaMA-based model using Hugging Face Transformers for crop-quality assessment.",
                "Generated AI-driven fertilizer recommendations for agricultural decision support.",
                "Built a web interface for crop image analysis and inference."
            ],
            "github": "https://github.com/srujan-vishwakarma/global-wheat-detection",
            "demo": "#",
            "badge": "Award Winning"
        },
        {
            "id": "mcp-fashion-analytics",
            "title": "MCP Fashion Conversational Analytics",
            "category": "GenAI & MLOps",
            "period": "TrendGully",
            "tagline": "Natural language interaction for enterprise fashion datasets using Model Context Protocol",
            "description": (
                "Created an MCP-powered conversational agent enabling non-technical stakeholders to query multi-million "
                "row fashion datasets in ClickHouse using natural language."
            ),
            "tech_stack": ["MCP Protocol", "ClickHouse", "FastAPI", "Python", "VLM", "MongoDB"],
            "features": [
                "Integrated ClickHouse analytics DB for ultra-fast query execution over large-scale fashion datasets.",
                "Implemented Model Context Protocol (MCP) tool bindings for seamless LLM context retrieval.",
                "Fine-tuned VLM (98% accuracy) for automatic attribute labeling."
            ],
            "github": "https://github.com/srujan-vishwakarma/mcp-fashion-analytics",
            "demo": "#",
            "badge": "Production AI"
        },
        {
            "id": "cloud-cost-agent",
            "title": "AWS Cloud Infrastructure Cost Optimization Agent",
            "category": "MLOps & Cloud",
            "period": "Ellucian",
            "tagline": "Multi-agent system reducing AWS cloud expenditure by 20% using SageMaker",
            "description": (
                "Developed a multi-agent recommendation ecosystem leveraging AWS SageMaker to analyze resource utilization, "
                "predict workload spikes, and automatically recommend right-sizing actions."
            ),
            "tech_stack": ["AWS SageMaker", "AWS Bedrock", "Multi-Agent Systems", "Python", "Predictive ML"],
            "features": [
                "Reduced cloud infrastructure costs by 20% through predictive ML scheduling.",
                "Designed multi-agent AWS service orchestrator.",
                "Fine-tuned code generation model for infrastructure-as-code automation."
            ],
            "github": "https://github.com/srujan-vishwakarma/aws-cost-agent",
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
    return templates.TemplateResponse("index.html", {"request": request, "profile": PROFILE_DATA})

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

@app.post("/api/chat")
async def ai_chat_assistant(query: ChatQuery):
    """
    Interactive Assistant Endpoint that answers recruiter/visitor questions about 
    Srujan's experience, skills, projects, and background.
    """
    msg = query.message.strip().lower()
    
    # Smart Intent Matching System based on Resume Context
    if any(k in msg for k in ["hello", "hi", "hey", "who are you"]):
        reply = (
            "Greetings! I am Srujan's Portfolio AI Assistant. "
            "Srujan is an AI Engineer specializing in Generative AI, Multi-Agent RAG systems, Vision-Language Models, and Cloud MLOps. "
            "Feel free to ask me about his work at TrendGully, Ellucian, projects like Agentic RAG, or his skills!"
        )
    elif any(k in msg for k in ["rag", "agentic", "langgraph", "vector"]):
        reply = (
            "Srujan architected a cutting-edge Microservices Agentic RAG Application! "
            "It uses LangGraph for autonomous reasoning and memory orchestration, Qdrant for vector search, Redis for caching, "
            "Ollama for local LLMs, and LangChain agents for async multi-source web research."
        )
    elif any(k in msg for k in ["vlm", "vision", "fashion", "trendgully", "accuracy"]):
        reply = (
            "At TrendGully (Junior AI Engineer), Srujan fine-tuned a Vision-Language Model (VLM) for apparel labeling and attribute "
            "classification, achieving an impressive 98% accuracy! He also migrated analytics to ClickHouse and built an MCP-powered conversational bot."
        )
    elif any(k in msg for k in ["ellucian", "aws", "cost", "cloud", "sagemaker"]):
        reply = (
            "During his Cloud Internship at Ellucian, Srujan built an AI-driven AWS infrastructure cost optimization dashboard "
            "using SageMaker & Multi-Agent systems, successfully cutting cloud costs by 20% and boosting utilization efficiency by 15%."
        )
    elif any(k in msg for k in ["wheat", "yolo", "intel", "hackathon"]):
        reply = (
            "Srujan developed 'Global Wheat Detection' (Intel AI for Youth award-winning project). "
            "It combines YOLO real-time computer vision, fine-tuned LLaMA models for crop quality assessment, and automated fertilizer recommendation."
        )
    elif any(k in msg for k in ["skills", "python", "tech stack", "tools"]):
        reply = (
            "Srujan's tech stack includes:\n"
            "• Languages: Python, SQL\n"
            "• AI/ML: PyTorch, Transformers, LangChain, LangGraph, CrewAI, FastAPI\n"
            "• GenAI: RAG, Multi-Agent Systems, Fine-tuning, Vector Search, MCP\n"
            "• Databases & MLOps: ClickHouse, Qdrant, Redis, MongoDB, AWS (SageMaker, Bedrock), Docker"
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
            f"Srujan Vishwakarma is an AI Engineer in Bangalore with strong expertise in Generative AI, RAG, and Cloud MLOps. "
            f"He has worked at TrendGully and Ellucian, built high-performance projects, and holds a 9.03 CGPA. "
            f"Try asking specifically about his 'RAG project', 'AWS experience', 'VLM work', or 'Skills'!"
        )

    return {"response": reply}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting Srujan's AI Portfolio Server on port {port}...")
    uvicorn.run("profile:app", host="0.0.0.0", port=port, reload=True)
