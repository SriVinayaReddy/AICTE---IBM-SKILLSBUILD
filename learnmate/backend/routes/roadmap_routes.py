"""
Roadmap API routes – generation, retrieval, and coaching.
"""
from flask import Blueprint, request, jsonify
from models.student import StudentProfile
from models.roadmap import Roadmap
from agents.roadmap_agent import RoadmapAgent
from agents.progress_agent import ProgressAgent
from utils.db import save_document, get_document, update_document

roadmap_bp = Blueprint("roadmap", __name__, url_prefix="/api/roadmaps")
roadmap_agent = RoadmapAgent()
progress_agent = ProgressAgent()


def _load_student(student_id: str):
    doc = get_document("students", student_id)
    if not doc:
        return None
    return StudentProfile.from_dict(doc)


def _load_roadmap(roadmap_id: str):
    doc = get_document("roadmaps", roadmap_id)
    if not doc:
        return None
    return Roadmap.from_dict(doc)


@roadmap_bp.route("/generate", methods=["POST"])
def generate_roadmap():
    """Generate a personalized roadmap for a student."""
    data = request.get_json() or {}
    student_id = data.get("student_id")
    if not student_id:
        return jsonify({"error": "student_id is required"}), 400

    profile = _load_student(student_id)
    if not profile:
        return jsonify({"error": "Student not found"}), 404

    if not profile.interests and not profile.skill_assessments:
        return jsonify({
            "error": "Please complete your profile with interests and skill assessment first."
        }), 400

    roadmap = roadmap_agent.generate_roadmap(profile)
    save_document("roadmaps", roadmap.to_dict(), roadmap.roadmap_id)

    # Link roadmap to student
    profile.current_roadmap_id = roadmap.roadmap_id
    save_document("students", profile.to_dict(), student_id)

    return jsonify({
        "roadmap_id": roadmap.roadmap_id,
        "roadmap": roadmap.to_dict(),
        "message": "Personalized roadmap generated successfully!",
    }), 201


@roadmap_bp.route("/<roadmap_id>", methods=["GET"])
def get_roadmap(roadmap_id):
    """Retrieve a roadmap by ID."""
    doc = get_document("roadmaps", roadmap_id)
    if not doc:
        return jsonify({"error": "Roadmap not found"}), 404
    return jsonify(doc), 200


@roadmap_bp.route("/<roadmap_id>/progress", methods=["PUT"])
def update_progress(roadmap_id):
    """Update progress on a roadmap step."""
    data = request.get_json() or {}
    student_id = data.get("student_id")
    step_number = data.get("step_number")
    completion_pct = data.get("completion_percentage", 0)
    notes = data.get("notes", "")

    if not student_id or step_number is None:
        return jsonify({"error": "student_id and step_number are required"}), 400

    profile = _load_student(student_id)
    if not profile:
        return jsonify({"error": "Student not found"}), 404

    roadmap = _load_roadmap(roadmap_id)
    if not roadmap:
        return jsonify({"error": "Roadmap not found"}), 404

    result = progress_agent.update_step_progress(
        profile, roadmap, int(step_number), int(completion_pct), notes
    )

    # Persist updates
    save_document("roadmaps", roadmap.to_dict(), roadmap_id)
    save_document("students", profile.to_dict(), student_id)

    return jsonify(result), 200


@roadmap_bp.route("/<roadmap_id>/adapt", methods=["POST"])
def adapt_roadmap(roadmap_id):
    """Adapt roadmap based on student feedback."""
    data = request.get_json() or {}
    student_id = data.get("student_id")
    feedback = data.get("feedback", "")

    if not student_id or not feedback:
        return jsonify({"error": "student_id and feedback are required"}), 400

    profile = _load_student(student_id)
    roadmap = _load_roadmap(roadmap_id)
    if not profile or not roadmap:
        return jsonify({"error": "Student or roadmap not found"}), 404

    updated_roadmap = roadmap_agent.adapt_roadmap(profile, roadmap, feedback)
    save_document("roadmaps", updated_roadmap.to_dict(), roadmap_id)

    return jsonify({
        "message": "Roadmap adapted based on your feedback.",
        "roadmap": updated_roadmap.to_dict(),
    }), 200


@roadmap_bp.route("/<roadmap_id>/report", methods=["GET"])
def weekly_report(roadmap_id):
    """Get the AI weekly progress report."""
    student_id = request.args.get("student_id")
    if not student_id:
        return jsonify({"error": "student_id query param required"}), 400

    profile = _load_student(student_id)
    roadmap = _load_roadmap(roadmap_id)
    if not profile or not roadmap:
        return jsonify({"error": "Student or roadmap not found"}), 404

    report = progress_agent.generate_weekly_report(profile, roadmap)
    return jsonify(report), 200


@roadmap_bp.route("/<roadmap_id>/recommendation", methods=["GET"])
def get_recommendation(roadmap_id):
    """Get AI adaptive learning recommendation."""
    student_id = request.args.get("student_id")
    if not student_id:
        return jsonify({"error": "student_id query param required"}), 400

    profile = _load_student(student_id)
    roadmap = _load_roadmap(roadmap_id)
    if not profile or not roadmap:
        return jsonify({"error": "Student or roadmap not found"}), 404

    rec = progress_agent.get_adaptive_recommendation(profile, roadmap)
    return jsonify(rec), 200


@roadmap_bp.route("/chat", methods=["POST"])
def chat_with_coach():
    """Conversational AI coaching endpoint."""
    data = request.get_json() or {}
    student_id = data.get("student_id")
    message = data.get("message", "")

    if not student_id or not message:
        return jsonify({"error": "student_id and message are required"}), 400

    profile = _load_student(student_id)
    if not profile:
        return jsonify({"error": "Student not found"}), 404

    response = roadmap_agent.chat_with_coach(profile, message)
    save_document("students", profile.to_dict(), student_id)

    return jsonify({"response": response, "student_id": student_id}), 200
