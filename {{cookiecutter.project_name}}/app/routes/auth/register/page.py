"""
Register Route - POST /auth/register

Handles new user registration.
"""

from fastapi import Body, HTTPException
from reroute import RouteBase
from reroute.decorators import rate_limit
# noinspection PyUnresolvedReferences
from logger import get_logger

from app.auth import hash_password
from app.auth.models import UserRegister, UserResponse, MessageResponse
{% if cookiecutter.database_type != 'none' %}from app.database import SessionLocal
from app.db_models.user import User
{% endif %}

logger = get_logger(__name__)


class RegisterRoutes(RouteBase):
    """
    Handles user registration.

    POST /auth/register - Create new user account
    """

    tag = "Auth"

    @rate_limit("3/min")
    def post(self, user_data: UserRegister = Body(...)):
        """
        Register a new user account.

        Returns user info on success (without password).
        """
        logger.info(f"Registration attempt for: {user_data.email}")
{% if cookiecutter.database_type != 'none' %}
        # Create database session
        db = SessionLocal()

        try:
            # Check for duplicate email
            existing = db.query(User).filter(User.email == user_data.email).first()
            if existing:
                raise HTTPException(status_code=400, detail="Email already registered")

            # Hash password
            password_hash = hash_password(user_data.password)

            # Create new user
            new_user = User(
                email=user_data.email,
                password_hash=password_hash,
                name=user_data.name
            )

            # Save to database
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            logger.info(f"User registered successfully: {user_data.email}")

            return {
                "message": "User registered successfully",
                "user": {
                    "id": new_user.id,
                    "email": new_user.email,
                    "name": new_user.name
                }
            }

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Registration failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Registration failed")
        finally:
            db.close()
{% else %}
        # In-memory storage (no database)
        # TODO: Implement proper database integration
        raise HTTPException(status_code=500, detail="Database not configured")
{% endif %}
