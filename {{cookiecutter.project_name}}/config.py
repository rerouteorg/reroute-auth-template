"""
{{ cookiecutter.project_name }} Configuration

Application-specific configuration settings.
"""

import os
from reroute import Config


class AppConfig(Config):
    """Application configuration"""

    # REROUTE Defaults - Hardcoded, not from cookiecutter
    HOST = "0.0.0.0"
    PORT = 7376
    AUTO_RELOAD = False  # Production mode

    # Framework Behavior
    VERBOSE_LOGGING = False  # Disable route registration logs

    # API Base Path Configuration
    # Uncomment and set to prefix all routes (e.g., "/api/v1")
    # API_BASE_PATH = "/api/v1"  # All routes will be under /api/v1/*
    API_BASE_PATH = ""  # No prefix (default)

    # CORS Configuration (applied globally)
    ENABLE_CORS = True
    CORS_ALLOW_ORIGINS = ["http://localhost:7376"]  # Default to localhost, change for production
    CORS_ALLOW_METHODS = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
    CORS_ALLOW_HEADERS = ["Content-Type", "Authorization", "X-Requested-With"]
    CORS_ALLOW_CREDENTIALS = False

    # OpenAPI/Swagger Documentation Configuration
    class OpenAPI:
        ENABLE = True  # Enable OpenAPI documentation

        # Documentation Endpoints
        DOCS_PATH = "/docs"            # Swagger UI endpoint (set to None to disable)
        REDOC_PATH = None              # ReDoc disabled by default
        JSON_PATH = "/openapi.json"    # Required when ENABLE=True

        # API Metadata
        TITLE = "{{ cookiecutter.project_name }}"  # API title
        VERSION = "1.0.0"              # API version
        DESCRIPTION = "{{ cookiecutter.project_name }} API - Built with REROUTE"  # API description

    # JWT Configuration for Authentication
    # REROUTE defaults - hardcoded, not from cookiecutter
    class JWT:
        ALGORITHM = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES = 30
        REFRESH_TOKEN_EXPIRE_DAYS = 7

        # User must provide this via environment variable
        SECRET = os.getenv("REROUTE_JWT_SECRET")
        if not SECRET:
            raise ValueError("REROUTE_JWT_SECRET environment variable not set!")

    # Load from env variables if needed
# AppConfig.load_from_env()
