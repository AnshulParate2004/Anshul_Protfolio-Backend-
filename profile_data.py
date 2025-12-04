"""
Anshul Parate's Profile Data
"""
from pydantic import BaseModel, HttpUrl
from typing import List, Dict

class ContactInfo(BaseModel):
    name: str = "Anshul Parate"
    role: str = "Generative AI Developer"
    email: str = "anshulnparate@gmail.com"
    phone: str = "+91 8208170566"
    portfolio: HttpUrl = "https://anshul-dev-profolio.vercel.app/"
    github: HttpUrl = "https://github.com/AnshulParate2004"
    linkedin: HttpUrl = "https://linkedin.com/in/anshulparate"

class Education(BaseModel):
    degree: str
    institution: str
    score: str
    period: str

class Project(BaseModel):
    name: str
    description: str
    highlights: List[str]
    technologies: List[str]
    demo_video: str
    github: str
    website: str

class Experience(BaseModel):
    title: str
    organization: str
    period: str
    responsibilities: List[str]

class AnshulProfile(BaseModel):
    contact: ContactInfo
    summary: str
    education: List[Education]
    technical_skills: Dict[str, List[str]]
    projects: List[Project]
    experience: List[Experience]
    achievements: List[str]

# Anshul's complete profile data
ANSHUL_PROFILE = AnshulProfile(
    contact=ContactInfo(),
    summary="""Full-Stack Generative AI Developer with deep expertise in RAG systems, LLMs, LangGraph, LangChain, Transformers, and advanced document understanding. Experienced in building production-grade pipelines with 94% semantic relevance, 35% faster inference on 1K+ daily queries, and 89% rockfall detection accuracy. Skilled across Computer Vision, MLOps, Prompt Engineering, and backend/frontend systems. Proven track record in delivering scalable GenAI solutions, leading technical teams, and driving measurable impact.""",
    
    education=[
        Education(
            degree="B.Tech CSE (AIML)",
            institution="Shri Ramdeobaba College of Engineering & Management",
            score="CGPA: 7.89",
            period="2023—Present"
        ),
        Education(
            degree="HSC (12th)",
            institution="Prerna International School, Vihirgaon",
            score="Percentage: 77.8%",
            period="2022"
        ),
        Education(
            degree="SSC (10th)",
            institution="Sanskar Vidya Sagar, Nagpur",
            score="Percentage: 80.2%",
            period="2020"
        )
    ],
    
    technical_skills={
        "Generative AI": ["Transformers", "LangGraph", "LangChain", "Qdrant", "Chroma", "Neo4j", "Unstructured.io", "Vertex AI"],
        "Machine Learning": ["PyTorch", "TensorFlow", "Computer Vision", "Scikit-learn"],
        "Backend Development": ["FastAPI", "Django REST Framework", "PostgreSQL", "MongoDB", "JWT/Auth Systems"],
        "Frontend Development": ["React.js", "UI/UX", "State Management", "Responsive Design", "TailwindCSS", "Figma"],
        "Cloud & DevOps": ["Docker", "Railway", "Render", "Git/GitHub", "CI/CD", "Model Deployment"],
        "Core Competencies": ["Prompt Engineering", "R&D", "Workflow Automation", "Leadership", "Problem Solving"]
    },
    
    projects=[
        Project(
            name="Multi-Modular RAG System",
            description="Solves AI gap in image/table extraction; supports 98 languages, 18 file formats",
            highlights=[
                "Built an LLM-driven chatbot using LangGraph, improving engagement by 40% over baseline bots",
                "Designed RAG pipelines using Unstructured.io achieving 92% accurate extraction across 1,000+ documents",
                "Retrieved real images + tables from PDFs, scans, docs, and 18+ formats with 94% precision"
            ],
            technologies=["React", "FastAPI", "Qdrant", "Chroma", "PostgreSQL", "Unstructured.io", "Python"],
            demo_video="https://www.youtube.com/watch?v=a9Haiu-e7ZU",
            github="https://github.com/AnshulParate2004/ChunkSmith",
            website="https://multi-modul-rag.vercel.app/"
        ),
        Project(
            name="Rockfall Detection System for Open-Pit Mines",
            description="SIH Round-1 Qualified Project",
            highlights=[
                "LiDAR drone mesh modeling identified 8–10% critical zones from full mine coverage",
                "PINN + YOLOv8 system achieved 89% accurate rockfall prediction using multi-sensor inputs",
                "FastAPI + OpenCV backend powering a React geo-dashboard with mobile alerts for 200 workers"
            ],
            technologies=["Python", "YOLOv8", "PyTorch", "OpenCV", "FastAPI", "React", "LiDAR", "PINN"],
            demo_video="https://www.youtube.com/watch?v=0eWDi7hRyVU",
            github="https://github.com/AnshulParate2004/GeoSentinel",
            website="https://sih-nu-liart.vercel.app/"
        ),
        Project(
            name="AI Chatbot with LangGraph & Semantic Storage",
            description="Agentic conversational flows with semantic memory",
            highlights=[
                "Built agentic conversational flows using LangGraph + FastAPI with Qdrant/Chroma",
                "Achieved 95% contextual memory retention with adaptive response generation",
                "Boosted user engagement by 40% through semantic pipelines"
            ],
            technologies=["LangGraph", "FastAPI", "Qdrant", "Chroma", "Python"],
            demo_video="",
            github="",
            website=""
        )
    ],
    
    experience=[
        Experience(
            title="Graphic Designer Lead",
            organization="Technical Club, RBU – Nagpur",
            period="2023–Present",
            responsibilities=[
                "Led a team of 6 developers/designers to build 5+ production-ready websites",
                "Designed complete UI/UX systems and 18 social media post sets for brand identity",
                "Managed Instagram growth achieving 150% engagement increase",
                "Organized 8+ technical events/workshops with 200+ participants"
            ]
        )
    ],
    
    achievements=[
        "Smart India Hackathon – Round 1 Qualifier",
        "Developed a high-accuracy image/table extraction system reducing data prep time by 60%",
        "Led a 6-member design team to increase Instagram engagement by 150%",
        "1st Place – School Drawing Competition"
    ]
)

# System prompt for the chatbot
SYSTEM_PROMPT = f"""You are an AI assistant representing Anshul Parate, a Generative AI Developer. 
Your role is to provide accurate information about Anshul's profile, projects, skills, and experience.

Key Information:
- Name: {ANSHUL_PROFILE.contact.name}
- Role: {ANSHUL_PROFILE.contact.role}
- Email: {ANSHUL_PROFILE.contact.email}
- Phone: {ANSHUL_PROFILE.contact.phone}
- Portfolio: {ANSHUL_PROFILE.contact.portfolio}
- GitHub: {ANSHUL_PROFILE.contact.github}
- LinkedIn: {ANSHUL_PROFILE.contact.linkedin}

When answering:
1. Be concise and informative
2. Always provide relevant links when discussing projects
3. Highlight key achievements and metrics
4. Use bullet points for clarity when listing items
5. Be enthusiastic about Anshul's work and capabilities

If asked about projects, provide:
- Project name and description
- Key highlights with metrics
- Technologies used
- Links to demo video, GitHub, and live website

If asked about skills, categorize them properly:
- Generative AI skills
- Machine Learning capabilities
- Backend and Frontend expertise
- Cloud and DevOps tools

Always be ready to provide contact information and portfolio links when requested.
"""
