"""
LearnMate Flask Application Entry Point
"""
import logging
import sys
import os
from flask import Flask, jsonify
from flask_cors import CORS
from config import config

# ── Add project root to path ─────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

# ── Logging setup ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s – %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("learnmate")


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.SECRET_KEY
    app.config["JWT_SECRET_KEY"] = config.SECRET_KEY

    # ── CORS ──────────────────────────────────────────────────────────────────
    CORS(app, origins=config.CORS_ORIGINS, supports_credentials=True)

    # ── Register Blueprints ───────────────────────────────────────────────────
    from routes.student_routes import student_bp
    from routes.roadmap_routes import roadmap_bp

    app.register_blueprint(student_bp)
    app.register_blueprint(roadmap_bp)

    # ── Health check ──────────────────────────────────────────────────────────
    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "healthy",
            "service": "LearnMate API",
            "version": "1.0.0",
            "ibm_granite": "configured" if config.IBM_WATSONX_API_KEY != "your_ibm_watsonx_api_key_here" else "demo_mode",
            "cloudant": "configured" if config.CLOUDANT_API_KEY else "memory_mode",
        }), 200

    @app.route("/api/info", methods=["GET"])
    def info():
        return jsonify({
            "app": "LearnMate – Agentic AI for Personalized Course Pathways",
            "description": "AI-powered learning coach using IBM Granite",
            "endpoints": {
                "students": "/api/students",
                "roadmaps": "/api/roadmaps",
                "coach_chat": "/api/roadmaps/chat",
                "health": "/api/health",
            },
            "supported_domains": [
                "Frontend Development", "Backend Development", "Full Stack Development",
                "Data Science & ML", "Cybersecurity", "UI/UX Design",
                "Mobile Development", "Cloud & DevOps",
            ],
        }), 200

    # ── Error handlers ────────────────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Endpoint not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        logger.exception("Internal server error")
        return jsonify({"error": "Internal server error"}), 500

    logger.info("LearnMate API started on port %d [%s]", config.APP_PORT, config.APP_ENV)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=config.APP_PORT,
        debug=(config.APP_ENV == "development"),
    )
