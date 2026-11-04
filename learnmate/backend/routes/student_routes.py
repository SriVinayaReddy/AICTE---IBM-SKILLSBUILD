"""
Student API routes – profile creation, onboarding, and management.
"""
from flask import Blueprint, request, jsonify
from models.student import StudentProfile, SKILL_DOMAINS, SKILL_LEVELS
from agents.assessment_agent import AssessmentAgent
from utils.db import save_document, get_document, update_document, list_documents

student_bp = Blueprint("student", __name__, url_prefix="/api/students")
assessment_agent = AssessmentAgent()


@student_bp.route("/", methods=["POST"])
def create_student():
    """Create a new student profile."""
    data = request.get_json() or {}
    profile = StudentProfile(
        name=data.get("name", ""),
        email=data.get("email", ""),
        interests=data.get("interests", []),
        learning_style=data.get("learning_style", "mixed"),
        weekly_hours=int(data.get("weekly_hours", 10)),
    )
    save_document("students", profile.to_dict(), profile.student_id)
    return jsonify({"student_id": profile.student_id, "profile": profile.to_dict()}), 201


@student_bp.route("/<student_id>", methods=["GET"])
def get_student(student_id):
    """Retrieve a student profile."""
    doc = get_document("students", student_id)
    if not doc:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(doc), 200


@student_bp.route("/<student_id>", methods=["PUT"])
def update_student(student_id):
    """Update a student profile."""
    data = request.get_json() or {}
    allowed = ["name", "email", "interests", "learning_style", "weekly_hours"]
    updates = {k: v for k, v in data.items() if k in allowed}
    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400
    success = update_document("students", student_id, updates)
    if not success:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"message": "Profile updated", "updates": updates}), 200


@student_bp.route("/<student_id>/assess", methods=["POST"])
def quick_assess(student_id):
    """Quick self-assessment for a domain."""
    doc = get_document("students", student_id)
    if not doc:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json() or {}
    domain = data.get("domain")
    self_rating = int(data.get("self_rating", 1))

    if domain not in SKILL_DOMAINS:
        return jsonify({"error": f"Invalid domain. Choose from: {SKILL_DOMAINS}"}), 400
    if self_rating not in range(1, 6):
        return jsonify({"error": "self_rating must be 1-5"}), 400

    profile = StudentProfile.from_dict(doc)
    assessment = assessment_agent.quick_assess(profile, domain, self_rating)
    save_document("students", profile.to_dict(), student_id)

    return jsonify({"assessment": assessment, "student_id": student_id}), 200


@student_bp.route("/<student_id>/assess/start", methods=["POST"])
def start_assessment(student_id):
    """Start a conversational skill assessment."""
    doc = get_document("students", student_id)
    if not doc:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json() or {}
    domain = data.get("domain")
    if not domain:
        return jsonify({"error": "domain is required"}), 400

    profile = StudentProfile.from_dict(doc)
    message = assessment_agent.start_assessment(profile, domain)
    save_document("students", profile.to_dict(), student_id)

    return jsonify({"message": message, "session_started": True}), 200


@student_bp.route("/<student_id>/assess/chat", methods=["POST"])
def continue_assessment(student_id):
    """Continue a conversational skill assessment."""
    doc = get_document("students", student_id)
    if not doc:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json() or {}
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"error": "message is required"}), 400

    profile = StudentProfile.from_dict(doc)
    result = assessment_agent.continue_assessment(profile, user_message)
    save_document("students", profile.to_dict(), student_id)

    return jsonify(result), 200


@student_bp.route("/<student_id>/goals", methods=["POST"])
def add_goal(student_id):
    """Add a learning goal to the student profile."""
    doc = get_document("students", student_id)
    if not doc:
        return jsonify({"error": "Student not found"}), 404

    data = request.get_json() or {}
    required = ["title", "description", "domain", "target_role", "timeline_weeks"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    profile = StudentProfile.from_dict(doc)
    profile.add_goal(
        title=data["title"],
        description=data["description"],
        domain=data["domain"],
        role=data["target_role"],
        weeks=int(data["timeline_weeks"]),
    )
    save_document("students", profile.to_dict(), student_id)

    return jsonify({"message": "Goal added", "goals": profile.goals}), 201


@student_bp.route("/domains", methods=["GET"])
def get_domains():
    """List all supported skill domains."""
    return jsonify({"domains": SKILL_DOMAINS, "levels": SKILL_LEVELS}), 200
