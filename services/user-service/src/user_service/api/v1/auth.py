from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.db.session import get_db
from user_service.schemas.user import UserLogin, UserResponse, TokenResponse
from user_service.services.user_service import UserService

from user_service.core.config import settings
from user_service.core.tokens import create_access_token

from user_service.api.dependencies import get_current_user
from user_service.models.user import User

router = APIRouter()

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)

    user = await service.authenticate_user(credentials)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user.id)

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

@router.get(
    "/me",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_authenticated_user(
    current_user: User = Depends(get_current_user),
):
    return current_user