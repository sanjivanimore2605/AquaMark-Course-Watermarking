from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.security.auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

def get_current_user_optional(token: Optional[str] = Depends(oauth2_scheme), token_query: Optional[str] = None, db: Session = Depends(get_db)) -> Optional[User]:
    actual_token = token or token_query
    if not actual_token:
        return None
    payload = decode_access_token(actual_token)
    if not payload:
        return None
    user_id = payload.get("sub")
    if not user_id:
        return None
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    return user

def get_current_user(user: Optional[User] = Depends(get_current_user_optional)) -> User:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials were not provided or have expired.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def get_current_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required for this action."
        )
    return user
