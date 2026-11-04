"""
Progress Tracker Agent – monitors student progress and adapts the roadmap dynamically.
"""
import logging
from datetime import datetime
from models.student import StudentProfile
from models.roadmap import Roadmap
from utils.granite_client import granite
from utils.db import update_document

logger = logging.getLogger(__name__)


class ProgressAgent:
    """Tracks learning progress and generates adaptive recommendations."""

    def update_step_progress(
        self,
        profile: StudentProfile,
        roadmap: Roadmap,
        step_number: int,
        completion_pct: int,
        notes: str = "",
    ) -> dict:
        """Update progress for a specific roadmap step."""
        # Clamp percentage
        completion_pct = max(0, min(100, completion_pct))

        # Determine status
        if completion_pct == 0:
            status = "not_started"
        elif completion_pct < 100:
            status = "in_progress"
        else:
            status = "completed"

        roadmap.update_step_status(step_number, status, completion_pct)

        # Log to student progress history
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "roadmap_id": roadmap.roadmap_id,
            "step_number": step_number,
            "status": status,
            "progress": completion_pct,
            "notes": notes,
        }
        profile.progress_log.append(log_entry)

        # Generate AI feedback for completed steps
        ai_feedback = ""
        if status == "completed":
            ai_feedback = self._generate_completion_feedback(profile, roadmap, step_number)

        return {
            "step_number": step_number,
            "status": status,
            "completion_percentage": completion_pct,
            "overall_progress": roadmap.overall_progress,
            "ai_feedback": ai_feedback,
            "next_step": self._get_next_step(roadmap, step_number),
        }

    def generate_weekly_report(self, profile: StudentProfile, roadmap: Roadmap) -> dict:
        """Generate an AI-powered weekly progress report."""
        recent_logs = [
            log for log in profile.progress_log[-14:]
            if log.get("roadmap_id") == roadmap.roadmap_id
        ]

        completed_steps = [s for s in roadmap.steps if s.get("status") == "completed"]
        in_progress = [s for s in roadmap.steps if s.get("status") == "in_progress"]
        not_started = [s for s in roadmap.steps if s.get("status") == "not_started"]

        prompt = f"""Generate a weekly learning progress report for a student.

Student: {profile.name or 'Student'}
Domain: {roadmap.domain}
Overall Progress: {roadmap.overall_progress}%
Completed Steps: {len(completed_steps)}/{len(roadmap.steps)}
Currently Working On: {in_progress[0]['title'] if in_progress else 'Nothing yet'}
Steps Remaining: {len(not_started)}
Recent Activity: {len(recent_logs)} sessions logged

Write a JSON report with:
{{
  "headline": "<one sentence summary>",
  "achievements": ["<achievement1>", "<achievement2>"],
  "focus_area": "<what to focus on this week>",
  "motivation": "<encouraging 2-sentence message>",
  "estimated_completion_weeks": <number>
}}"""

        raw = granite.generate(prompt)
        report_data = self._extract_json(raw)

        if not report_data:
            weeks_left = max(1, (len(not_started) + len(in_progress)) * 2)
            report_data = {
                "headline": f"You're {roadmap.overall_progress}% through your {roadmap.domain} journey!",
                "achievements": [f"Completed {len(completed_steps)} learning modules"],
                "focus_area": in_progress[0]["title"] if in_progress else "Start your next step",
                "motivation": (
                    "Keep pushing forward — every hour of learning compounds over time. "
                    "You're building skills that will last a lifetime."
                ),
                "estimated_completion_weeks": weeks_left,
            }

        return {
            **report_data,
            "overall_progress": roadmap.overall_progress,
            "completed_steps": len(completed_steps),
            "total_steps": len(roadmap.steps),
            "roadmap_title": roadmap.title,
        }

    def get_adaptive_recommendation(self, profile: StudentProfile, roadmap: Roadmap) -> dict:
        """Use Granite to recommend the next best action for the student."""
        current_step = next(
            (s for s in roadmap.steps if s.get("status") == "in_progress"),
            roadmap.steps[0] if roadmap.steps else None,
        )
        if not current_step:
            return {"recommendation": "Start your first learning step!", "action": "begin_roadmap"}

        days_since_activity = self._days_since_last_activity(profile, roadmap.roadmap_id)

        prompt = f"""A student is learning {roadmap.domain} at {roadmap.skill_level} level.
Current step: "{current_step['title']}" — {current_step['completion_percentage']}% done.
Days since last activity: {days_since_activity}.
Weekly hours available: {profile.weekly_hours}.

Give a specific, actionable next-step recommendation as JSON:
{{
  "recommendation": "<specific action to take today>",
  "resource": "<specific resource name or activity>",
  "time_needed_minutes": <number>,
  "priority": "high|medium|low",
  "tip": "<one practical study tip>"
}}"""

        raw = granite.generate(prompt)
        rec = self._extract_json(raw)
        if not rec:
            rec = {
                "recommendation": f"Continue with '{current_step['title']}'",
                "resource": current_step.get("courses", [{}])[0].get("title", "Your current course"),
                "time_needed_minutes": 45,
                "priority": "high",
                "tip": "Break your session into 25-minute focused blocks with 5-minute breaks.",
            }
        return rec

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _generate_completion_feedback(self, profile, roadmap, step_number) -> str:
        step = next((s for s in roadmap.steps if s.get("step_number") == step_number), None)
        if not step:
            return "Great job completing this step!"
        prompt = (
            f"A student just completed '{step['title']}' in their {roadmap.domain} roadmap. "
            f"Write 2 sentences of enthusiastic, specific encouragement and preview the next step."
        )
        return granite.generate(prompt)

    def _get_next_step(self, roadmap: Roadmap, current_step_number: int) -> dict | None:
        for step in roadmap.steps:
            if step.get("step_number", 0) > current_step_number:
                if step.get("status") != "completed":
                    return {
                        "step_number": step["step_number"],
                        "title": step["title"],
                        "estimated_weeks": step.get("estimated_weeks", 2),
                    }
        return None

    def _days_since_last_activity(self, profile: StudentProfile, roadmap_id: str) -> int:
        relevant = [
            log for log in profile.progress_log if log.get("roadmap_id") == roadmap_id
        ]
        if not relevant:
            return 999
        try:
            last = relevant[-1]["timestamp"]
            last_dt = datetime.fromisoformat(last.replace("Z", "+00:00"))
            delta = datetime.utcnow() - last_dt.replace(tzinfo=None)
            return delta.days
        except Exception:
            return 0

    def _extract_json(self, text: str) -> dict | None:
        import json
        import re
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if not match:
            return None
        try:
            return json.loads(match.group())
        except Exception:
            return None
