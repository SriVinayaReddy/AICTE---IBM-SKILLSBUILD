"""
Student data model – profile, skill levels, and learning preferences.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional
import uuid


SKILL_DOMAINS = [
    "Frontend Development",
    "Backend Development",
    "Full Stack Development",
    "Data Science & ML",
    "Cybersecurity",
    "UI/UX Design",
    "Mobile Development",
    "Cloud & DevOps",
    "Blockchain",
    "Game Development",
]

SKILL_LEVELS = ["beginner", "intermediate", "advanced", "expert"]

LEARNING_STYLES = ["visual", "reading", "hands-on", "video", "mixed"]


@dataclass
class SkillAssessment:
    domain: str
    level: str  # beginner | intermediate | advanced | expert
    score: float  # 0.0 – 1.0
    assessed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class LearningGoal:
    title: str
    description: str
    target_domain: str
    target_role: str          # e.g. "Frontend Engineer"
    timeline_weeks: int       # desired completion in weeks
    priority: str = "high"   # high | medium | low
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class StudentProfile:
    student_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    email: str = ""
    interests: list[str] = field(default_factory=list)
    skill_assessments: list[dict] = field(default_factory=list)
    goals: list[dict] = field(default_factory=list)
    learning_style: str = "mixed"
    weekly_hours: int = 10       # hours per week available
    current_roadmap_id: Optional[str] = None
    conversation_history: list[dict] = field(default_factory=list)
    progress_log: list[dict] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "StudentProfile":
        data = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**data)

    def add_skill(self, domain: str, level: str, score: float):
        """Add or update a skill assessment."""
        assessment = SkillAssessment(domain=domain, level=level, score=score)
        # Replace existing
        self.skill_assessments = [
            s for s in self.skill_assessments if s.get("domain") != domain
        ]
        self.skill_assessments.append(assessment.to_dict())

    def add_goal(self, title: str, description: str, domain: str, role: str, weeks: int):
        goal = LearningGoal(
            title=title, description=description, target_domain=domain,
            target_role=role, timeline_weeks=weeks
        )
        self.goals.append(goal.to_dict())

    def add_message(self, role: str, content: str):
        """Append a message to conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        })
        # Keep last 20 messages to stay within token limits
        self.conversation_history = self.conversation_history[-20:]

    def get_primary_domain(self) -> str:
        """Return the highest-scored or first-interest domain."""
        if self.skill_assessments:
            best = max(self.skill_assessments, key=lambda s: s.get("score", 0))
            return best["domain"]
        return self.interests[0] if self.interests else "General Programming"

    def get_skill_level(self, domain: str) -> str:
        for s in self.skill_assessments:
            if s.get("domain") == domain:
                return s.get("level", "beginner")
        return "beginner"
