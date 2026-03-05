"""
{{ cookiecutter.project_name }} Configuration

Application-specific configuration settings.
"""

from reroute import Config


class AppConfig(Config):
    """Application configuration"""

    # Server Configuration
    HOST = "{{ cookiecutter.host }}"
    PORT = {{ cookiecutter.port }}

    # Framework Behavior
    VERBOSE_LOGGING = False  # Disable route registration logs
    AUTO_RELOAD = {% if cookiecutter.reload == 'true' or cookiecutter.reload == 'True' %}True{% else %}False{% endif %}

    # API Base Path Configuration
    # Uncomment and set to prefix all routes (e.g., "/api/v1")
    # API_BASE_PATH = "/api/v1"  # All routes will be under /api/v1/*
    API_BASE_PATH = ""  # No prefix (default)

    # CORS Configuration (applied globally)
    ENABLE_CORS = True
    CORS_ALLOW_ORIGINS = ["http://localhost:{{ cookiecutter.port }}"]  # Default to localhost, change for production
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
    class JWT:
        SECRET = "{{ cookiecutter.jwt_secret }}"
        ALGORITHM = "{{ cookiecutter.jwt_algorithm }}"
        ACCESS_TOKEN_EXPIRE_MINUTES = {{ cookiecutter.access_token_expire_minutes }}
        REFRESH_TOKEN_EXPIRE_DAYS = {{ cookiecutter.refresh_token_expire_days }}

    # Load from env variables if needed
# AppConfig.load_from_env()
