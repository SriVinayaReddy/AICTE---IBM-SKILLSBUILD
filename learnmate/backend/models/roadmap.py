"""
Course and Roadmap data models.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Course:
    course_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    provider: str = ""          # e.g. Coursera, IBM, YouTube
    url: str = ""
    domain: str = ""
    skill_level: str = "beginner"
    duration_hours: int = 0
    topics: list[str] = field(default_factory=list)
    is_free: bool = True
    rating: float = 0.0
    description: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RoadmapStep:
    step_number: int
    title: str
    description: str
    courses: list[dict] = field(default_factory=list)
    skills_gained: list[str] = field(default_factory=list)
    estimated_weeks: int = 1
    status: str = "not_started"   # not_started | in_progress | completed
    completion_percentage: int = 0
    resources: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Roadmap:
    roadmap_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    student_id: str = ""
    title: str = ""
    domain: str = ""
    target_role: str = ""
    skill_level: str = "beginner"
    total_weeks: int = 0
    steps: list[dict] = field(default_factory=list)
    ai_summary: str = ""
    ai_tips: list[str] = field(default_factory=list)
    overall_progress: int = 0       # 0–100 %
    is_active: bool = True
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Roadmap":
        data = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**data)

    def calculate_progress(self) -> int:
        """Recalculate overall progress from step completion percentages."""
        if not self.steps:
            return 0
        total = sum(s.get("completion_percentage", 0) for s in self.steps)
        self.overall_progress = total // len(self.steps)
        return self.overall_progress

    def update_step_status(self, step_number: int, status: str, pct: int):
        for step in self.steps:
            if step.get("step_number") == step_number:
                step["status"] = status
                step["completion_percentage"] = pct
                break
        self.calculate_progress()
        self.updated_at = datetime.utcnow().isoformat() + "Z"
