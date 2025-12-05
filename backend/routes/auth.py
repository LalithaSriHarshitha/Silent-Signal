"""Authentication routes"""
from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import secrets
import structlog

from backend.database import get_db
from backend.integrations.workos_client import workos_auth
from backend.models.user import User
from backend.models.session import Session as UserSession
from backend.schemas.auth import TokenResponse

logger = structlog.get_logger()
router = APIRouter()


@router.get("/login")
async def login(request: Request):
    """Initiate WorkOS login flow"""
    from fastapi.responses import RedirectResponse
    
    try:
        state = secrets.token_urlsafe(32)
        authorization_url = workos_auth.get_authorization_url(state=state)
        
        # Store state in session for verification
        request.session["oauth_state"] = state
        
        # Redirect user to WorkOS login page
        return RedirectResponse(url=authorization_url)
    except ValueError as e:
        # WorkOS not configured - redirect to demo mode
        logger.warning("WorkOS not configured, using demo mode")
        raise HTTPException(
            status_code=503,
            detail="Authentication service not configured. Please add WorkOS API keys to .env file or use demo mode."
        )


@router.get("/callback")
async def auth_callback(
    code: str,
    state: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """Handle WorkOS OAuth callback"""
    # Verify state
    stored_state = request.session.get("oauth_state")
    if not stored_state or stored_state != state:
        raise HTTPException(status_code=400, detail="Invalid state parameter")
    
    try:
        # Authenticate with WorkOS
        user_data = await workos_auth.authenticate_with_code(code)
        
        # Find or create user
        user = db.query(User).filter(User.workos_id == user_data["workos_id"]).first()
        
        if not user:
            user = User(
                workos_id=user_data["workos_id"],
                email=user_data["email"],
                full_name=user_data["full_name"],
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info("New user created", user_id=user.id, email=user.email)
        
        # Create session
        session_token = secrets.token_urlsafe(32)
        user_session = UserSession(
            user_id=user.id,
            session_token=session_token,
            expires_at=datetime.utcnow() + timedelta(days=7)
        )
        db.add(user_session)
        db.commit()
        
        # Set session cookie
        response = Response()
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=7 * 24 * 60 * 60  # 7 days
        )
        
        logger.info("User logged in", user_id=user.id)
        
        # Redirect to dashboard after successful login
        from fastapi.responses import RedirectResponse
        response = RedirectResponse(url="/dashboard", status_code=302)
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite="lax",
            max_age=7 * 24 * 60 * 60  # 7 days
        )
        return response
        
    except Exception as e:
        logger.error("Authentication callback failed", error=str(e))
        raise HTTPException(status_code=500, detail="Authentication failed")


@router.post("/logout")
async def logout(request: Request, db: Session = Depends(get_db)):
    """Logout user and invalidate session"""
    session_token = request.cookies.get("session_token")
    
    if session_token:
        user_session = db.query(UserSession).filter(
            UserSession.session_token == session_token
        ).first()
        
        if user_session:
            db.delete(user_session)
            db.commit()
    
    response = Response(content="Logged out successfully")
    response.delete_cookie("session_token")
    
    return response


@router.get("/me")
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    """Get current authenticated user"""
    session_token = request.cookies.get("session_token")
    
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    user_session = db.query(UserSession).filter(
        UserSession.session_token == session_token
    ).first()
    
    if not user_session or user_session.is_expired:
        raise HTTPException(status_code=401, detail="Session expired")
    
    user = db.query(User).filter(User.id == user_session.user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user
