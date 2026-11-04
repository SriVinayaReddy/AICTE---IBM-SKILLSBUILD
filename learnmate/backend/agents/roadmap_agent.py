"""
Roadmap Agent – uses IBM Granite to generate personalized course roadmaps.
"""
import logging
import json
import re
from models.student import StudentProfile
from models.roadmap import Roadmap, RoadmapStep
from utils.granite_client import granite
from utils.course_catalog import get_courses_for_level, get_all_courses_for_domain

logger = logging.getLogger(__name__)


ROADMAP_SYSTEM_PROMPT = """You are LearnMate's Roadmap Builder, powered by IBM Granite.
Your task is to create a detailed, structured learning roadmap for a student.
You must return a JSON object with this exact structure:
{
  "title": "<roadmap title>",
  "domain": "<domain>",
  "target_role": "<target job role>",
  "total_weeks": <number>,
  "ai_summary": "<2-3 sentence encouraging summary>",
  "ai_tips": ["<tip1>", "<tip2>", "<tip3>"],
  "steps": [
    {
      "step_number": 1,
      "title": "<step title>",
      "description": "<what they'll learn and why it matters>",
      "skills_gained": ["skill1", "skill2"],
      "estimated_weeks": <weeks for this step>,
      "resources": [
        {"type": "article|video|practice", "title": "<title>", "url": "<url>"}
      ]
    }
  ]
}
Create 5-8 progressive steps from their current level to the target role.
Each step should build logically on the previous one."""


class RoadmapAgent:
    """Generates and adapts personalized learning roadmaps using IBM Granite."""

    def generate_roadmap(self, profile: StudentProfile) -> Roadmap:
        """Create a full personalized roadmap for the student."""
        domain = profile.get_primary_domain()
        level = profile.get_skill_level(domain)
        goal = profile.goals[0] if profile.goals else None
        target_role = goal["target_role"] if goal else f"{domain} Developer"
        timeline = goal["timeline_weeks"] if goal else profile.weekly_hours * 4

        prompt = self._build_roadmap_prompt(profile, domain, level, target_role, timeline)
        raw_response = granite.generate(prompt)

        roadmap_data = self._parse_roadmap_json(raw_response)
        if not roadmap_data:
            logger.warning("Granite didn't return valid JSON, using structured fallback.")
            roadmap_data = self._build_fallback_roadmap(profile, domain, level, target_role)

        # Inject curated courses into steps
        roadmap_data = self._inject_courses(roadmap_data, domain, level)

        roadmap = Roadmap(
            student_id=profile.student_id,
            title=roadmap_data.get("title", f"{domain} Learning Path"),
            domain=roadmap_data.get("domain", domain),
            target_role=roadmap_data.get("target_role", target_role),
            skill_level=level,
            total_weeks=roadmap_data.get("total_weeks", timeline),
            steps=roadmap_data.get("steps", []),
            ai_summary=roadmap_data.get("ai_summary", ""),
            ai_tips=roadmap_data.get("ai_tips", []),
        )
        return roadmap

    def adapt_roadmap(self, profile: StudentProfile, roadmap: Roadmap, feedback: str) -> Roadmap:
        """Adapt an existing roadmap based on student feedback/progress."""
        prompt = f"""A student is on step {self._current_step(roadmap)} of their {roadmap.domain} roadmap.
Their feedback: "{feedback}"
Overall progress: {roadmap.overall_progress}%

Suggest 2-3 specific adjustments to improve their roadmap.
Return JSON: {{"adjustments": [{{"step_number": <n>, "change": "<description>", "reason": "<why>"}}],
"encouragement": "<motivational message>"}}"""

        raw = granite.generate(prompt)
        adaptation = self._extract_json(raw)

        if adaptation:
            roadmap.ai_tips = [adaptation.get("encouragement", "")] + [
                a.get("change", "") for a in adaptation.get("adjustments", [])
            ]
        roadmap.updated_at = __import__("datetime").datetime.utcnow().isoformat() + "Z"
        return roadmap

    def chat_with_coach(self, profile: StudentProfile, user_message: str) -> str:
        """Conversational coaching using Granite chat model."""
        system = f"""You are LearnMate, an AI learning coach. The student is studying {profile.get_primary_domain()}.
Their current level: {profile.get_skill_level(profile.get_primary_domain())}.
Their progress: {self._get_progress_summary(profile)}.
Answer their question helpfully. Be concise and actionable."""

        messages = [{"role": "system", "content": system}]
        for msg in profile.conversation_history[-8:]:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": user_message})

        response = granite.chat(messages)
        profile.add_message("user", user_message)
        profile.add_message("assistant", response)
        return response

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------
    def _build_roadmap_prompt(self, profile, domain, level, target_role, timeline):
        goal_context = ""
        if profile.goals:
            g = profile.goals[0]
            goal_context = f"\nGoal: {g.get('description', '')}"

        skills_context = ""
        if profile.skill_assessments:
            skills_context = "Known skills: " + ", ".join(
                f"{s['domain']}({s['level']})" for s in profile.skill_assessments
            )

        return f"""{ROADMAP_SYSTEM_PROMPT}

Student Profile:
- Name: {profile.name or 'Student'}
- Domain of Interest: {domain}
- Current Level: {level}
- Target Role: {target_role}
- Available Time: {profile.weekly_hours} hours/week
- Timeline: {timeline} weeks{goal_context}
- Learning Style: {profile.learning_style}
- {skills_context}

Generate the personalized roadmap JSON now:"""

    def _parse_roadmap_json(self, text: str) -> dict | None:
        """Extract and parse JSON roadmap from Granite output."""
        # Try to find JSON block
        match = re.search(r'\{.*"steps"\s*:\s*\[.*\]\s*\}', text, re.DOTALL)
        if not match:
            return None
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

        # Try cleaning common issues
        try:
            cleaned = re.sub(r',\s*([}\]])', r'\1', match.group())
            return json.loads(cleaned)
        except Exception:
            return None

    def _extract_json(self, text: str) -> dict | None:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if not match:
            return None
        try:
            return json.loads(match.group())
        except Exception:
            return None

    def _inject_courses(self, roadmap_data: dict, domain: str, start_level: str) -> dict:
        """Attach curated catalog courses to roadmap steps."""
        levels = ["beginner", "intermediate", "advanced", "expert"]
        level_idx = levels.index(start_level) if start_level in levels else 0
        steps = roadmap_data.get("steps", [])

        for i, step in enumerate(steps):
            # Escalate level every 2 steps
            current_level = levels[min(level_idx + i // 2, len(levels) - 1)]
            courses = get_courses_for_level(domain, current_level)[:2]
            step["courses"] = [
                {
                    "title": c["title"],
                    "provider": c["provider"],
                    "url": c["url"],
                    "duration_hours": c.get("duration_hours", 0),
                    "is_free": c.get("is_free", True),
                    "rating": c.get("rating", 0),
                    "topics": c.get("topics", []),
                }
                for c in courses
            ]
            step["status"] = "not_started"
            step["completion_percentage"] = 0

        roadmap_data["steps"] = steps
        return roadmap_data

    def _build_fallback_roadmap(self, profile, domain, level, target_role) -> dict:
        """Structured fallback when Granite is unavailable."""
        levels_progression = {
            "beginner": ["Fundamentals", "Core Concepts", "Basic Projects",
                         "Intermediate Topics", "Real Projects", "Advanced Topics", "Portfolio"],
            "intermediate": ["Skill Deepening", "Advanced Concepts", "Real-World Projects",
                              "Best Practices", "System Design", "Specialization"],
            "advanced": ["Expert Topics", "Architecture", "Open Source",
                         "Leadership", "Mentoring"],
        }
        step_titles = levels_progression.get(level, levels_progression["beginner"])
        steps = []
        for idx, title in enumerate(step_titles, 1):
            steps.append({
                "step_number": idx,
                "title": f"{domain}: {title}",
                "description": f"Master {title.lower()} concepts in {domain}.",
                "skills_gained": [f"{domain} - {title}"],
                "estimated_weeks": 2,
                "resources": [],
            })

        return {
            "title": f"{domain} → {target_role} Roadmap",
            "domain": domain,
            "target_role": target_role,
            "total_weeks": len(steps) * 2,
            "ai_summary": (
                f"This roadmap will take you from {level} to a confident {target_role}. "
                f"With {profile.weekly_hours} hours/week, you'll build real skills step by step."
            ),
            "ai_tips": [
                "Consistency beats intensity — show up every day.",
                "Build projects, don't just watch videos.",
                "Join a community to accelerate learning.",
            ],
            "steps": steps,
        }

    def _current_step(self, roadmap: Roadmap) -> int:
        for step in roadmap.steps:
            if step.get("status") == "in_progress":
                return step.get("step_number", 1)
        return 1

    def _get_progress_summary(self, profile: StudentProfile) -> str:
        if not profile.progress_log:
            return "just getting started"
        recent = profile.progress_log[-1]
        return f"{recent.get('progress', 0)}% complete on their current step"
