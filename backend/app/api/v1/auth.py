from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.schemas.schemas import UserRegister, UserLogin, Token, UserResponse
from app.security.auth import get_password_hash, verify_password, create_access_token
from app.security.deps import get_current_user
from app.services.audit import log_audit_event

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    
    # Password strength check
    if len(user_in.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long.")
    
    # Determine role: make first user admin, rest instructors
    user_count = db.query(User).count()
    role = "admin" if user_count == 0 else "instructor"
    
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        institution=user_in.institution,
        role=role,
        is_active=True,
        is_verified=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    log_audit_event(db, "USER_REGISTER", actor_id=user.id, details={"email": user.email, "role": user.role})
    return user

@router.post("/login", response_model=Token)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        log_audit_event(db, "LOGIN_FAILED", details={"email": login_data.email}, status="FAILED")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User account is deactivated.")
        
    access_token = create_access_token(data={"sub": user.id, "email": user.email, "role": user.role})
    log_audit_event(db, "USER_LOGIN", actor_id=user.id, details={"email": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "institution": user.institution,
            "role": user.role
        }
    }

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
