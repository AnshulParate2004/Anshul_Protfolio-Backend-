"""
LangGraph Agent for Anshul's Portfolio Chatbot
Fast, memory-efficient conversational agent with 10-message history limit
"""
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from config import settings
from profile_data import ANSHUL_PROFILE, SYSTEM_PROMPT
import json

# Define the state structure
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    
class AnshulChatAgent:
    """
    LangGraph-based chat agent with:
    - Fast response times using Gemini Flash
    - Memory limited to last 10 conversations
    - Pydantic-validated profile data
    - Optimized for quick lookups
    """
    
    def __init__(self):
        # Initialize fast Gemini model
        self.llm = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=settings.GEMINI_TEMPERATURE,
            max_output_tokens=settings.GEMINI_MAX_OUTPUT_TOKENS,
        )
        
        # Build the graph
        self.graph = self._build_graph()
        self.app = self.graph.compile()
        
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("agent", self._agent_node)
        
        # Set entry point
        workflow.set_entry_point("agent")
        
        # Add edge to END
        workflow.add_edge("agent", END)
        
        return workflow
    
    def _agent_node(self, state: AgentState) -> dict:
        """
        Main agent node that processes messages
        Maintains only last 10 messages for efficiency
        """
        messages = state["messages"]
        
        # Trim to last 10 messages (excluding system message)
        if len(messages) > settings.MAX_CONVERSATION_HISTORY + 1:
            # Keep system message + last 10 messages
            messages = [messages[0]] + messages[-(settings.MAX_CONVERSATION_HISTORY):]
        
        # Invoke LLM
        response = self.llm.invoke(messages)
        
        return {"messages": [response]}
    
    def get_profile_context(self, query: str) -> str:
        """
        Quick lookup of relevant profile information
        Optimized for common queries
        """
        query_lower = query.lower()
        
        # Contact information
        if any(word in query_lower for word in ["contact", "email", "phone", "reach", "linkedin", "github"]):
            return f"""
Contact Information:
- Email: {ANSHUL_PROFILE.contact.email}
- Phone: {ANSHUL_PROFILE.contact.phone}
- Portfolio: {ANSHUL_PROFILE.contact.portfolio}
- GitHub: {ANSHUL_PROFILE.contact.github}
- LinkedIn: {ANSHUL_PROFILE.contact.linkedin}
"""
        
        # Projects
        if any(word in query_lower for word in ["project", "rag", "rockfall", "chatbot", "portfolio"]):
            projects_info = "\n\n".join([
                f"**{p.name}**\n{p.description}\n"
                f"Demo: {p.demo_video}\nGitHub: {p.github}\nWebsite: {p.website}"
                for p in ANSHUL_PROFILE.projects
            ])
            return f"Projects:\n{projects_info}"
        
        # Skills
        if any(word in query_lower for word in ["skill", "technology", "tech stack", "tools"]):
            skills_info = "\n".join([
                f"**{category}:** {', '.join(skills)}"
                for category, skills in ANSHUL_PROFILE.technical_skills.items()
            ])
            return f"Technical Skills:\n{skills_info}"
        
        # Education
        if any(word in query_lower for word in ["education", "degree", "college", "university"]):
            edu_info = "\n".join([
                f"- {e.degree} at {e.institution} ({e.score}) | {e.period}"
                for e in ANSHUL_PROFILE.education
            ])
            return f"Education:\n{edu_info}"
        
        # Experience
        if any(word in query_lower for word in ["experience", "work", "job", "position"]):
            exp_info = "\n".join([
                f"**{e.title}** at {e.organization} ({e.period})\n" +
                "\n".join([f"  • {r}" for r in e.responsibilities])
                for e in ANSHUL_PROFILE.experience
            ])
            return f"Experience:\n{exp_info}"
        
        # Achievements
        if any(word in query_lower for word in ["achievement", "award", "accomplishment"]):
            ach_info = "\n".join([f"• {a}" for a in ANSHUL_PROFILE.achievements])
            return f"Achievements:\n{ach_info}"
        
        return ""
    
    def chat(self, message: str, session_messages: list = None) -> str:
        """
        Process a chat message with fast response
        
        Args:
            message: User's input message
            session_messages: Previous messages in session (auto-trimmed to 10)
        
        Returns:
            AI response string
        """
        # Initialize messages with system prompt
        if session_messages is None or len(session_messages) == 0:
            messages = [SystemMessage(content=SYSTEM_PROMPT)]
        else:
            messages = session_messages
            # Ensure system message is first
            if not isinstance(messages[0], SystemMessage):
                messages.insert(0, SystemMessage(content=SYSTEM_PROMPT))
        
        # Add context if relevant
        context = self.get_profile_context(message)
        if context:
            enhanced_message = f"{message}\n\nRelevant Information:\n{context}"
        else:
            enhanced_message = message
        
        # Add user message
        messages.append(HumanMessage(content=enhanced_message))
        
        # Trim to maintain memory limit (system + last 10 messages)
        if len(messages) > settings.MAX_CONVERSATION_HISTORY + 1:
            messages = [messages[0]] + messages[-(settings.MAX_CONVERSATION_HISTORY):]
        
        # Run through graph
        result = self.app.invoke({"messages": messages})
        
        # Extract response
        response = result["messages"][-1].content
        
        return response, messages + [AIMessage(content=response)]
    
    def get_quick_info(self, info_type: str) -> dict:
        """
        Get specific information quickly without LLM
        
        Args:
            info_type: One of ['contact', 'projects', 'skills', 'education', 'experience', 'achievements']
        
        Returns:
            Dictionary with requested information
        """
        info_map = {
            "contact": ANSHUL_PROFILE.contact.dict(),
            "projects": [p.dict() for p in ANSHUL_PROFILE.projects],
            "skills": ANSHUL_PROFILE.technical_skills,
            "education": [e.dict() for e in ANSHUL_PROFILE.education],
            "experience": [e.dict() for e in ANSHUL_PROFILE.experience],
            "achievements": ANSHUL_PROFILE.achievements,
            "summary": ANSHUL_PROFILE.summary
        }
        
        return info_map.get(info_type, {})
