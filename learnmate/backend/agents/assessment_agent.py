"""
Assessment Agent – uses IBM Granite to evaluate student skills via conversation.
"""
import logging
import json
import re
from models.student import StudentProfile, SKILL_DOMAINS, SKILL_LEVELS
from utils.granite_client import granite

logger = logging.getLogger(__name__)


SYSTEM_PROMPT = """You are LearnMate, an expert educational AI coach powered by IBM Granite.
Your goal is to assess a student's current skill level through friendly conversation.
Ask targeted, relevant questions to understand:
1. Their current knowledge and experience in their chosen domain
2. Projects they've built or worked on
3. Concepts they are comfortable with
4. Areas where they feel weak

Be concise, encouraging, and professional. After gathering enough information,
provide a JSON skill assessment in this exact format:
{
  "domain": "<domain>",
  "level": "<beginner|intermediate|advanced|expert>",
  "score": <0.0-1.0>,
  "strengths": ["...", "..."],
  "gaps": ["...", "..."],
  "recommended_start": "<topic to start with>"
}
"""


class AssessmentAgent:
    """Conducts skill assessment dialogue using IBM Granite."""

    def __init__(self):
        self.system_prompt = SYSTEM_PROMPT

    def start_assessment(self, profile: StudentProfile, domain: str) -> str:
        """Begin the assessment conversation for a given domain."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {
                "role": "user",
                "content": (
                    f"Hi! I'm {profile.name or 'a student'} and I want to learn {domain}. "
                    f"I have about {profile.weekly_hours} hours per week to study."
                ),
            },
        ]
        response = granite.chat(messages)
        profile.add_message("user", f"I want to learn {domain}. I have {profile.weekly_hours}h/week.")
        profile.add_message("assistant", response)
        return response

    def continue_assessment(self, profile: StudentProfile, user_message: str) -> dict:
        """Continue the assessment with the student's reply."""
        # Build message history
        messages = [{"role": "system", "content": self.system_prompt}]
        for msg in profile.conversation_history[-10:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_message})

        response = granite.chat(messages)
        profile.add_message("user", user_message)
        profile.add_message("assistant", response)

        # Try to extract structured assessment if Granite included it
        assessment = self._extract_assessment(response)
        return {
            "message": response,
            "assessment": assessment,
            "assessment_complete": assessment is not None,
        }

    def quick_assess(self, profile: StudentProfile, domain: str, self_rating: int) -> dict:
        """
        Quick assessment via self-rating (1–5 scale) without full dialogue.
        Uses Granite to elaborate on the assessment.
        """
        level_map = {1: "beginner", 2: "beginner", 3: "intermediate", 4: "advanced", 5: "expert"}
        score_map = {1: 0.1, 2: 0.3, 3: 0.5, 4: 0.75, 5: 0.95}
        level = level_map.get(self_rating, "beginner")
        score = score_map.get(self_rating, 0.1)

        prompt = f"""A student rated themselves {self_rating}/5 in {domain} ({level} level).
Generate a brief skill assessment JSON:
{{
  "domain": "{domain}",
  "level": "{level}",
  "score": {score},
  "strengths": [<2 likely strengths at this level>],
  "gaps": [<2 likely knowledge gaps to address>],
  "recommended_start": "<best starting topic>"
}}
Return ONLY valid JSON, no other text."""

        raw = granite.generate(prompt)
        assessment = self._extract_assessment(raw)
        if not assessment:
            assessment = {
                "domain": domain,
                "level": level,
                "score": score,
                "strengths": [f"Basic {domain} awareness"],
                "gaps": [f"Practical {domain} projects", "Advanced concepts"],
                "recommended_start": f"Introduction to {domain}",
            }

        profile.add_skill(domain, assessment["level"], assessment["score"])
        return assessment

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _extract_assessment(self, text: str) -> dict | None:
        """Parse JSON assessment block from Granite response."""
        # Look for JSON object in the text
        match = re.search(r'\{[^{}]*"domain"[^{}]*\}', text, re.DOTALL)
        if not match:
            return None
        try:
            data = json.loads(match.group())
            required = {"domain", "level", "score"}
            if required.issubset(data.keys()):
                return data
        except json.JSONDecodeError:
            pass
        return None
