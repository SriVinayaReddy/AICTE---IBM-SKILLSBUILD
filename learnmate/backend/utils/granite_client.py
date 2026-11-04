"""
IBM Granite AI Client - wraps ibm-watsonx-ai SDK for LearnMate.
Handles text generation, chat, and embedding calls to IBM Granite models.
Falls back to demo mode when the SDK is not installed or credentials are missing.
"""
import logging
from typing import Optional
from config import config

# Optional IBM SDK - graceful fallback when not installed
try:
    from ibm_watsonx_ai import APIClient, Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference
    from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
    IBM_SDK_AVAILABLE = True
except ImportError:
    IBM_SDK_AVAILABLE = False

logger = logging.getLogger(__name__)


class GraniteClient:
    """Singleton wrapper around IBM watsonx.ai Granite models."""

    _instance: Optional["GraniteClient"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        if not IBM_SDK_AVAILABLE:
            logger.warning("ibm-watsonx-ai SDK not installed - running in DEMO mode. "
                           "Install with: pip install ibm-watsonx-ai")
            self.instruct_model = None
            self.chat_model = None
            return

        try:
            credentials = Credentials(
                url=config.IBM_WATSONX_URL,
                api_key=config.IBM_WATSONX_API_KEY,
            )
            self.client = APIClient(credentials)
            self.project_id = config.IBM_WATSONX_PROJECT_ID

            # Instruct model for roadmap generation
            self.instruct_model = ModelInference(
                model_id=config.IBM_GRANITE_MODEL_ID,
                credentials=credentials,
                project_id=self.project_id,
                params={
                    GenParams.MAX_NEW_TOKENS: 1024,
                    GenParams.TEMPERATURE: 0.7,
                    GenParams.TOP_P: 0.9,
                    GenParams.STOP_SEQUENCES: ["###", "<|endoftext|>"],
                },
            )

            # Chat model for conversational coach
            self.chat_model = ModelInference(
                model_id=config.IBM_GRANITE_CHAT_MODEL,
                credentials=credentials,
                project_id=self.project_id,
                params={
                    GenParams.MAX_NEW_TOKENS: 512,
                    GenParams.TEMPERATURE: 0.6,
                    GenParams.TOP_P: 0.85,
                },
            )
            logger.info("IBM Granite client initialised successfully.")
        except Exception as exc:
            logger.error("Failed to initialise IBM Granite client: %s", exc)
            self.instruct_model = None
            self.chat_model = None

    # ------------------------------------------------------------------
    # Text generation (instruct)
    # ------------------------------------------------------------------
    def generate(self, prompt: str, max_tokens: int = 1024) -> str:
        """Generate text using the instruct Granite model."""
        if not self.instruct_model:
            return self._fallback_generate(prompt)
        try:
            response = self.instruct_model.generate_text(prompt=prompt)
            return response.strip()
        except Exception as exc:
            logger.error("Granite generate error: %s", exc)
            return self._fallback_generate(prompt)

    # ------------------------------------------------------------------
    # Chat (conversational)
    # ------------------------------------------------------------------
    def chat(self, messages: list) -> str:
        """Send a chat message list to Granite chat model."""
        if not self.chat_model:
            return self._fallback_chat(messages)
        try:
            prompt = self._build_chat_prompt(messages)
            response = self.chat_model.generate_text(prompt=prompt)
            return response.strip()
        except Exception as exc:
            logger.error("Granite chat error: %s", exc)
            return self._fallback_chat(messages)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _build_chat_prompt(self, messages: list) -> str:
        """Convert OpenAI-style messages into Granite chat format."""
        parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                parts.append("<|system|>\n" + content)
            elif role == "user":
                parts.append("<|user|>\n" + content)
            elif role == "assistant":
                parts.append("<|assistant|>\n" + content)
        parts.append("<|assistant|>")
        return "\n".join(parts)

    def _fallback_generate(self, prompt: str) -> str:
        """Deterministic fallback when IBM Granite is unavailable (demo mode)."""
        logger.warning("Using fallback generation (IBM Granite unavailable).")
        # Smart demo responses based on prompt keywords
        prompt_lower = prompt.lower()
        if "roadmap" in prompt_lower or "steps" in prompt_lower:
            return self._demo_roadmap_json(prompt)
        if "assessment" in prompt_lower or "skill" in prompt_lower:
            return self._demo_assessment_json(prompt)
        return (
            "[DEMO MODE - IBM Granite unavailable] "
            "Please configure IBM_WATSONX_API_KEY and IBM_WATSONX_PROJECT_ID "
            "in your .env file to enable AI-powered responses."
        )

    def _fallback_chat(self, messages: list) -> str:
        last = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "")
        return (
            "Hi! I am LearnMate, your AI learning coach (running in Demo Mode). "
            "To enable full IBM Granite AI responses, add your IBM_WATSONX_API_KEY "
            "and IBM_WATSONX_PROJECT_ID to the .env file. "
            "Your message was: '" + last[:100] + "'"
        )

    def _demo_roadmap_json(self, prompt: str) -> str:
        """Return a realistic demo roadmap JSON for local testing."""
        import re
        domain = "Frontend Development"
        for d in ["Cybersecurity", "UI/UX Design", "Data Science", "Backend", "Cloud", "Mobile"]:
            if d.lower() in prompt.lower():
                domain = d
                break
        return '''{
  "title": "''' + domain + ''' Learning Path",
  "domain": "''' + domain + '''",
  "target_role": "''' + domain + ''' Developer",
  "total_weeks": 12,
  "ai_summary": "This roadmap will take you from beginner to job-ready in ''' + domain + '''. Each step builds on the previous one with hands-on projects.",
  "ai_tips": [
    "Consistency beats intensity - study 1 hour daily rather than 7 hours on weekends.",
    "Build real projects at every stage, do not just watch tutorials.",
    "Join communities like Discord servers and local meetups to accelerate learning."
  ],
  "steps": [
    {
      "step_number": 1,
      "title": "Foundations of ''' + domain + '''",
      "description": "Learn the core fundamentals and set up your development environment.",
      "skills_gained": ["Core Concepts", "Environment Setup", "Basic Syntax"],
      "estimated_weeks": 2,
      "resources": [
        {"type": "video", "title": "IBM SkillsBuild - Free Courses", "url": "https://skillsbuild.org"},
        {"type": "article", "title": "Official Documentation", "url": "https://developer.mozilla.org"}
      ]
    },
    {
      "step_number": 2,
      "title": "Core Skills Development",
      "description": "Deep-dive into the essential tools and techniques used by professionals.",
      "skills_gained": ["Practical Tools", "Industry Best Practices", "Problem Solving"],
      "estimated_weeks": 3,
      "resources": [
        {"type": "practice", "title": "freeCodeCamp Exercises", "url": "https://freecodecamp.org"}
      ]
    },
    {
      "step_number": 3,
      "title": "Build Your First Project",
      "description": "Apply your knowledge by building a complete real-world project from scratch.",
      "skills_gained": ["Project Architecture", "Debugging", "Version Control"],
      "estimated_weeks": 2,
      "resources": [
        {"type": "practice", "title": "GitHub - Start your repo", "url": "https://github.com"}
      ]
    },
    {
      "step_number": 4,
      "title": "Intermediate Concepts",
      "description": "Advance your skills with intermediate-level topics and patterns.",
      "skills_gained": ["Advanced Patterns", "Performance", "Testing"],
      "estimated_weeks": 3,
      "resources": [
        {"type": "video", "title": "Coursera / IBM Specialisation", "url": "https://coursera.org"}
      ]
    },
    {
      "step_number": 5,
      "title": "Portfolio & Job Readiness",
      "description": "Build a portfolio project, write your resume, and prepare for interviews.",
      "skills_gained": ["Portfolio Building", "Interview Prep", "Networking"],
      "estimated_weeks": 2,
      "resources": [
        {"type": "article", "title": "LinkedIn Profile Optimisation", "url": "https://linkedin.com"}
      ]
    }
  ]
}'''

    def _demo_assessment_json(self, prompt: str) -> str:
        return '''{
  "domain": "Frontend Development",
  "level": "beginner",
  "score": 0.25,
  "strengths": ["Enthusiasm to learn", "Basic HTML awareness"],
  "gaps": ["Practical project experience", "JavaScript fundamentals"],
  "recommended_start": "HTML & CSS Foundations"
}'''


# Module-level singleton
granite = GraniteClient()
