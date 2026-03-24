import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import Token, UserCreate, UserResponse
from ..security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)

logger = logging.getLogger("users-service")

router = APIRouter(prefix="/users", tags=["users"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


@router.get("/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    logger.info(
        "users_listed", 
        extra={
            "event": "users_listed",
            "result_count": len(users),
        },
    )

    return users


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if email is None:
            logger.warning(
                "invalid_token_subject",
                extra={
                    "event": "invalid_token_subject",
                },
            )
            raise credentials_exception
    except JWTError:
        logger.warning(
            "invalid_or_expired_token",
            extra={
                "event": "invalid_or_expired_token",
            },
        )
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        logger.warning(
            "authenticated_user_not_found",
            extra={
                "event": "authenticated_user_not_found",
                "email": email,
            },
        )
        raise credentials_exception

    logger.info(
        "authenticated_user_loaded",
        extra={
            "event": "authenticated_user_loaded",
            "user_id": user.id,
            "email": user.email,
            "user_name": user.name,
        },
    )

    return user


@router.get("/secure")
def secure_route(current_user: User = Depends(get_current_user)):
    logger.info(
        "secure_route_accessed",
        extra={
            "event": "secure_route_accessed",
            "user_id": current_user.id,
            "email": current_user.email,
            "user_name": current_user.name,
        },
    )

    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
    }


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        logger.warning(
            "user_not_found",
            extra={
                "event": "user_not_found",
                "user_id": user_id,
            },
        )
        raise HTTPException(status_code=404, detail="User not found")

    logger.info(
        "user_retrieved",
        extra={
            "event": "user_retrieved",
            "user_id": user.id,
            "email": user.email,
            "user_name": user.name,
        },
    )

    return user


@router.post("/", response_model=UserResponse, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == payload.email).first()

    if existing_user:
        logger.warning(
            "user_creation_conflict",
            extra={
                "event": "user_creation_conflict",
                "email": payload.email,
            },
        )
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=payload.name,
        email=payload.email,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info(
        "user_created",
        extra={
            "event": "user_created",
            "user_id": user.id,
            "email": user.email,
            "user_name": user.name,
        },
    )

    return user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        logger.warning(
            "login_failed",
            extra={
                "event": "login_failed",
                "email": form_data.username,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(data={"sub": user.email})

    logger.info(
        "login_succeeded",
        extra={
            "event": "login_succeeded",
            "user_id": user.id,
            "email": user.email,
            "user_name": user.name,
        },
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
