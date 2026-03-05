"""
Login Route - POST /auth/login

Authenticates user and returns JWT tokens.
"""

from fastapi import Body, HTTPException
from reroute import RouteBase
from reroute.decorators import rate_limit
# noinspection PyUnresolvedReferences
from logger import get_logger

from app.auth import create_access_token, create_refresh_token, verify_password
from app.auth.models import UserLogin, TokenResponse
{% if cookiecutter.database != 'none' %}from app.database import SessionLocal
from app.db_models.user import User
{% endif %}

logger = get_logger(__name__)


class LoginRoutes(RouteBase):
    """
    Handles user authentication.

    POST /auth/login - Authenticate and get tokens
    """

    tag = "Auth"

    @rate_limit("5/min")
    def post(self, credentials: UserLogin = Body(...)):
        """
        Authenticate user and return JWT tokens.

        Returns access_token and refresh_token on success.
        """
        logger.info(f"Login attempt for: {credentials.email}")
{% if cookiecutter.database != 'none' %}
        # Create database session
        db = SessionLocal()

        try:
            # Lookup user by email
            user = db.query(User).filter(User.email == credentials.email).first()

            if not user or not verify_password(credentials.password, user.password_hash):
                logger.warning(f"Failed login attempt for: {credentials.email}")
                raise HTTPException(status_code=401, detail="Invalid email or password")

            # Create tokens
            token_data = {"sub": str(user.id), "email": user.email}
            access_token = create_access_token(token_data)
            refresh_token = create_refresh_token(token_data)

            logger.info(f"Login successful for: {credentials.email}")

            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer",
                "expires_in": 1800
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Login failed")
        finally:
            db.close()
{% else %}
        # In-memory storage (no database)
        # TODO: Implement proper database integration
        raise HTTPException(status_code=500, detail="Database not configured")
{% endif %}
