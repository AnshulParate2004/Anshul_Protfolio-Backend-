"""
Simplified Chat Agent using Google Generative AI directly
No LangChain/LangGraph dependencies for Vercel deployment
"""
import google.generativeai as genai
from typing import List, Dict, Optional
from config import settings
from profile_data import ANSHUL_PROFILE, SYSTEM_PROMPT

class AnshulChatAgent:
    """
    Lightweight chat agent using Google Generative AI SDK directly
    - Fast response times using Gemini Flash
    - Memory limited to last 10 conversations
    - No heavy dependencies
    """
    
    def __init__(self):
        # Configure Gemini
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        
        # Initialize model with generation config
        self.generation_config = {
            "temperature": settings.GEMINI_TEMPERATURE,
            "max_output_tokens": settings.GEMINI_MAX_OUTPUT_TOKENS,
        }
        
        self.model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL,
            generation_config=self.generation_config,
        )
    
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
    
    def format_history(self, messages: List[Dict]) -> List[Dict]:
        """
        Convert message history to Gemini format
        Format: [{"role": "user", "parts": ["text"]}, {"role": "model", "parts": ["text"]}]
        """
        formatted = []
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content", "")
            
            if role == "system":
                # Skip system messages, they're added to the first user message
                continue
            elif role == "user":
                formatted.append({"role": "user", "parts": [content]})
            elif role == "assistant" or role == "model":
                formatted.append({"role": "model", "parts": [content]})
        
        return formatted
    
    def chat(self, message: str, session_messages: Optional[List[Dict]] = None) -> tuple[str, List[Dict]]:
        """
        Process a chat message with fast response
        
        Args:
            message: User's input message
            session_messages: Previous messages in session (auto-trimmed to 10)
        
        Returns:
            Tuple of (AI response string, updated messages list)
        """
        # Initialize messages
        if session_messages is None or len(session_messages) == 0:
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        else:
            messages = session_messages.copy()
            # Ensure system message is first
            if not messages or messages[0].get("role") != "system":
                messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT})
        
        # Add context if relevant
        context = self.get_profile_context(message)
        if context:
            enhanced_message = f"{message}\n\nRelevant Information:\n{context}"
        else:
            enhanced_message = message
        
        # Trim to maintain memory limit (system + last 10 messages)
        if len(messages) > settings.MAX_CONVERSATION_HISTORY + 1:
            system_msg = messages[0]
            messages = [system_msg] + messages[-(settings.MAX_CONVERSATION_HISTORY):]
        
        # Format history for Gemini
        history = self.format_history(messages[1:])  # Exclude system message from history
        
        # Start chat with system prompt and history
        chat = self.model.start_chat(history=history)
        
        # Send message with system context
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {enhanced_message}"
        response = chat.send_message(full_prompt)
        
        # Add new messages to history
        messages.append({"role": "user", "content": message})
        messages.append({"role": "assistant", "content": response.text})
        
        # Trim again after adding new messages
        if len(messages) > settings.MAX_CONVERSATION_HISTORY + 1:
            system_msg = messages[0]
            messages = [system_msg] + messages[-(settings.MAX_CONVERSATION_HISTORY):]
        
        return response.text, messages
    
    def get_quick_info(self, info_type: str) -> Optional[Dict]:
        """
        Get specific information quickly without LLM
        
        Args:
            info_type: One of ['contact', 'projects', 'skills', 'education', 'experience', 'achievements', 'summary']
        
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
        
        return info_map.get(info_type)
