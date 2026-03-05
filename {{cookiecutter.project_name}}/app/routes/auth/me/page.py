"""
Me Route - GET /auth/me

Returns current authenticated user info.
"""

from fastapi import Header, HTTPException
from reroute import RouteBase
from reroute.decorators import cache
# noinspection PyUnresolvedReferences
from logger import get_logger

from app.auth import verify_token
from app.auth.models import UserResponse
{% if cookiecutter.database_type != 'none' %}from app.database import SessionLocal
from app.db_models.user import User
{% endif %}

logger = get_logger(__name__)


class MeRoutes(RouteBase):
    """
    Handles current user info retrieval.

    GET /auth/me - Get authenticated user profile (requires token)
    """

    tag = "Auth"

    @cache(duration=60)
    def get(self, authorization: str = Header(None)):
        """
        Get current authenticated user profile.

        Requires valid Bearer token in Authorization header.
        """
        # Extract and verify token
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Not authenticated")

        token = authorization.split(" ")[1]
        payload = verify_token(token, token_type="access")

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        user_id = payload.get("sub")
        email = payload.get("email")

        logger.info(f"Profile accessed by: {email}")
{% if cookiecutter.database_type != 'none' %}
        # Fetch full user data from database
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == int(user_id)).first()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            return {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat()
            }

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching user profile: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch user profile")
        finally:
            db.close()
{% else %}
        # In-memory storage (no database)
        # TODO: Implement proper database integration
        return {
            "id": user_id,
            "email": email
        }
{% endif %}
