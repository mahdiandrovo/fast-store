
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.db.session import get_db
from user_service.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from user_service.services.user_service import (
    EmailAlreadyRegisteredError,
    UserNotFoundError,
    UserService,
)

from user_service.api.dependencies import get_current_user
from user_service.models.user import User


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


# 1. CREATE USER
@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    service = UserService(db)

    try:
        return await service.create_user(user_data)

    except EmailAlreadyRegisteredError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


# 2. GET ALL USERS
@router.get(
    "",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
)
async def get_users(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = UserService(db)

    return await service.get_users(
        skip=skip,
        limit=limit,
    )


# 3. GET USER BY ID
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = UserService(db)

    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to access this user's information.",
        )

    try:
        return await service.get_user(user_id)

    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


# 4. UPDATE USER
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = UserService(db)

    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to update this user's information.",
        )

    try:
        return await service.update_user(
            user_id=user_id,
            user_data=user_data,
        )

    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except EmailAlreadyRegisteredError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc