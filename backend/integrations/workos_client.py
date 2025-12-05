"""WorkOS authentication client"""
import workos
from workos import WorkOSClient
from typing import Optional, Dict
import structlog

from backend.config import settings

logger = structlog.get_logger()

# Initialize WorkOS client only if API key is provided
workos_client = None
if settings.WORKOS_API_KEY and settings.WORKOS_CLIENT_ID:
    try:
        workos_client = WorkOSClient(
            api_key=settings.WORKOS_API_KEY,
            client_id=settings.WORKOS_CLIENT_ID
        )
        logger.info("WorkOS client initialized successfully")
    except Exception as e:
        logger.warning("WorkOS client initialization failed", error=str(e))
else:
    logger.warning("WorkOS credentials not configured, authentication disabled")


class WorkOSAuth:
    """WorkOS authentication helper"""
    
    @staticmethod
    def get_authorization_url(state: Optional[str] = None) -> str:
        """Generate authorization URL for OAuth flow"""
        if not workos_client:
            raise ValueError("WorkOS client not initialized")
        try:
            authorization_url = workos_client.user_management.get_authorization_url(
                provider="authkit",
                redirect_uri=settings.WORKOS_REDIRECT_URI,
                state=state,
            )
            return authorization_url
        except Exception as e:
            logger.error("Failed to generate authorization URL", error=str(e))
            raise
    
    @staticmethod
    async def authenticate_with_code(code: str) -> Dict:
        """Exchange authorization code for user profile"""
        try:
            profile = workos_client.user_management.authenticate_with_code(
                code=code,
            )
            
            user_data = {
                "workos_id": profile.user.id,
                "email": profile.user.email,
                "full_name": f"{profile.user.first_name or ''} {profile.user.last_name or ''}".strip(),
                "access_token": profile.access_token,
                "refresh_token": profile.refresh_token,
            }
            
            logger.info("User authenticated", workos_id=user_data["workos_id"])
            return user_data
            
        except Exception as e:
            logger.error("Authentication failed", error=str(e))
            raise
    
    @staticmethod
    async def get_user_profile(access_token: str) -> Dict:
        """Get user profile from access token"""
        try:
            user = workos_client.user_management.get_user(access_token)
            return {
                "workos_id": user.id,
                "email": user.email,
                "full_name": f"{user.first_name or ''} {user.last_name or ''}".strip(),
            }
        except Exception as e:
            logger.error("Failed to get user profile", error=str(e))
            raise
    
    @staticmethod
    async def refresh_token(refresh_token: str) -> Dict:
        """Refresh access token"""
        try:
            result = workos_client.user_management.authenticate_with_refresh_token(
                refresh_token=refresh_token,
            )
            return {
                "access_token": result.access_token,
                "refresh_token": result.refresh_token,
            }
        except Exception as e:
            logger.error("Token refresh failed", error=str(e))
            raise


workos_auth = WorkOSAuth()
