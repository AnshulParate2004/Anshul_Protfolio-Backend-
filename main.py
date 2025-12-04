"""
FastAPI Backend for Anshul Parate Portfolio Chatbot
Minimal dependencies version for Vercel deployment
No LangChain/LangGraph - uses Google Generative AI SDK directly
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from functools import lru_cache

# Import settings and agent
from config import settings
from agent import AnshulChatAgent
from profile_data import ANSHUL_PROFILE

# Don't validate on module import - let it fail gracefully on first request
# This prevents crashes during Vercel cold starts

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Lightweight AI-powered portfolio assistant for Anshul Parate"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="User's message")
    session_id: Optional[str] = Field(default=settings.DEFAULT_SESSION_ID, description="Session identifier")

class ChatResponse(BaseModel):
    response: str = Field(..., description="AI assistant's response")
    success: bool = Field(default=True)
    timestamp: datetime = Field(default_factory=datetime.now)
    message_count: int = Field(..., description="Number of messages in conversation")

class QuickInfoRequest(BaseModel):
    info_type: str = Field(..., description="Type: contact, projects, skills, education, experience, achievements, summary")

class SessionInfo(BaseModel):
    session_id: str
    message_count: int
    last_activity: datetime

# Store session data (messages + timestamps)
class SessionData:
    def __init__(self):
        self.messages = []
        self.last_activity = datetime.now()
    
    def update_activity(self):
        self.last_activity = datetime.now()
    
    def is_expired(self, timeout_minutes: int) -> bool:
        return datetime.now() - self.last_activity > timedelta(minutes=timeout_minutes)

# Session storage
sessions: Dict[str, SessionData] = {}

# Initialize agent (singleton)
@lru_cache()
def get_agent():
    """Cached agent initialization for faster responses"""
    return AnshulChatAgent()

def get_or_create_session(session_id: str) -> SessionData:
    """Get existing session or create new one"""
    if session_id not in sessions:
        sessions[session_id] = SessionData()
    else:
        sessions[session_id].update_activity()
    return sessions[session_id]

def cleanup_expired_sessions():
    """Remove expired sessions"""
    expired = [
        sid for sid, data in sessions.items()
        if data.is_expired(settings.SESSION_TIMEOUT_MINUTES)
    ]
    for sid in expired:
        del sessions[sid]

@app.on_event("startup")
async def startup_event():
    """Initialize agent on startup"""
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"🤖 Model: {settings.GEMINI_MODEL}")
    print(f"💾 Memory: Last {settings.MAX_CONVERSATION_HISTORY} messages per session")
    print(f"⚡ Minimal dependencies for Vercel")
    
    # Pre-initialize agent (with error handling)
    try:
        get_agent()
        print(f"✅ Ready to chat about Anshul Parate!")
    except Exception as e:
        print(f"⚠️ Agent initialization warning: {e}")
        print("⚠️ Check that GOOGLE_API_KEY is set in Vercel environment variables")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "status": "running",
        "profile": {
            "name": ANSHUL_PROFILE.contact.name,
            "role": ANSHUL_PROFILE.contact.role,
            "portfolio": str(ANSHUL_PROFILE.contact.portfolio)
        },
        "features": [
            "Fast responses with Gemini Flash",
            "10-message conversation memory",
            "Direct Google Generative AI integration",
            "Minimal dependencies for Vercel",
            "Quick info endpoints"
        ],
        "endpoints": {
            "chat": "/chat",
            "quick_info": "/quick-info",
            "reset": "/reset",
            "health": "/health",
            "sessions": "/sessions",
            "profile": "/profile",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    cleanup_expired_sessions()
    return {
        "status": "healthy",
        "model": settings.GEMINI_MODEL,
        "active_sessions": len(sessions),
        "memory_limit": settings.MAX_CONVERSATION_HISTORY,
        "timestamp": datetime.now()
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Fast chat endpoint with 10-message memory
    
    Optimized for quick responses using:
    - Gemini Flash model
    - Direct Google Generative AI SDK
    - Efficient message trimming
    - Context pre-fetching for relevant queries
    """
    try:
        # Get or create session
        session_data = get_or_create_session(request.session_id)
        
        # Get agent (cached)
        agent = get_agent()
        
        # Process message
        response, updated_messages = agent.chat(
            request.message,
            session_data.messages
        )
        
        # Update session with trimmed messages
        session_data.messages = updated_messages
        session_data.update_activity()
        
        # Count messages (exclude system message)
        message_count = len([m for m in session_data.messages if m.get("role") != "system"])
        
        return ChatResponse(
            response=response,
            success=True,
            message_count=message_count
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.post("/quick-info")
async def quick_info(request: QuickInfoRequest):
    """
    Get specific profile information without LLM (instant response)
    
    Available types:
    - contact: Contact details and links
    - projects: All projects with links
    - skills: Technical skills by category
    - education: Educational background
    - experience: Work experience
    - achievements: Achievements and awards
    - summary: Professional summary
    """
    try:
        agent = get_agent()
        info = agent.get_quick_info(request.info_type)
        
        if not info:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid info_type. Choose from: contact, projects, skills, education, experience, achievements, summary"
            )
        
        return {
            "type": request.info_type,
            "data": info,
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/profile")
async def get_full_profile():
    """Get complete profile information"""
    return {
        "profile": ANSHUL_PROFILE.dict(),
        "success": True
    }

@app.post("/reset")
async def reset_conversation(session_id: str = settings.DEFAULT_SESSION_ID):
    """Reset conversation memory for a session"""
    try:
        if session_id in sessions:
            del sessions[session_id]
            message = f"✅ Conversation reset for session: {session_id}"
        else:
            message = f"ℹ️ No active conversation found for session: {session_id}"
        
        return {
            "message": message,
            "success": True
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting conversation: {str(e)}")

@app.get("/sessions")
async def list_sessions():
    """List all active sessions with details"""
    cleanup_expired_sessions()
    
    session_list = [
        SessionInfo(
            session_id=sid,
            message_count=len([m for m in data.messages if m.get("role") != "system"]),
            last_activity=data.last_activity
        )
        for sid, data in sessions.items()
    ]
    
    return {
        "sessions": session_list,
        "count": len(session_list),
        "memory_limit_per_session": settings.MAX_CONVERSATION_HISTORY
    }

@app.delete("/sessions/cleanup")
async def cleanup_sessions():
    """Manually cleanup expired sessions"""
    before_count = len(sessions)
    cleanup_expired_sessions()
    after_count = len(sessions)
    
    return {
        "message": "Cleanup completed",
        "removed": before_count - after_count,
        "active": after_count
    }

# Vercel serverless function handler
handler = app
