"""
LearnMate Configuration – loads all settings from environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # IBM watsonx.ai / Granite
    IBM_WATSONX_API_KEY: str = os.getenv("IBM_WATSONX_API_KEY", "")
    IBM_WATSONX_PROJECT_ID: str = os.getenv("IBM_WATSONX_PROJECT_ID", "")
    IBM_WATSONX_URL: str = os.getenv("IBM_WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
    IBM_GRANITE_MODEL_ID: str = os.getenv("IBM_GRANITE_MODEL_ID", "ibm/granite-13b-instruct-v2")
    IBM_GRANITE_CHAT_MODEL: str = os.getenv("IBM_GRANITE_CHAT_MODEL", "ibm/granite-13b-chat-v2")
    IBM_GRANITE_EMBED_MODEL: str = os.getenv("IBM_GRANITE_EMBED_MODEL", "ibm/slate-125m-english-rtrvr")

    # IBM Cloudant
    CLOUDANT_URL: str = os.getenv("CLOUDANT_URL", "")
    CLOUDANT_API_KEY: str = os.getenv("CLOUDANT_API_KEY", "")
    CLOUDANT_DB_NAME: str = os.getenv("CLOUDANT_DB_NAME", "learnmate_db")

    # Flask App
    APP_PORT: int = int(os.getenv("APP_PORT", "5000"))
    APP_ENV: str = os.getenv("APP_ENV", "development")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "learnmate-dev-secret")
    JWT_EXPIRY_HOURS: int = int(os.getenv("JWT_EXPIRY_HOURS", "24"))
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


config = Config()
