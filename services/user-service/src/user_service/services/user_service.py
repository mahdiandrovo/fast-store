
from sqlalchemy.ext.asyncio import AsyncSession

from user_service.core.security import hash_password
from user_service.models.user import User
from user_service.repositories.user_repository import UserRepository
from user_service.schemas.user import UserCreate, UserUpdate

from user_service.core.security import verify_password
from user_service.schemas.user import UserLogin


class UserNotFoundError(Exception):
    """Raised when a requested user does not exist."""


class EmailAlreadyRegisteredError(Exception):
    """Raised when an email address is already registered."""


class UserService:

    def __init__(self, db: AsyncSession):
        self.repository = UserRepository(db)
        self.db = db

    async def create_user(self, user_data: UserCreate) -> User:
        try:
            # Check whether the email is already registered.
            existing_user = await self.repository.get_by_email(
                user_data.email
            )

            if existing_user:
                raise EmailAlreadyRegisteredError(
                    "This email address is already registered."
                )

            # Hash the password before storing it
            user_dict = {
                "name": user_data.name,
                "email": user_data.email,
                "phone_number": user_data.phone_number,
                "country": user_data.country,
                "password_hash": hash_password(user_data.password),
            }

            user = await self.repository.create(user_dict)

            await self.db.commit()

            return user

        except Exception:
            await self.db.rollback()
            raise

    async def get_user(self, user_id: int) -> User:
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise UserNotFoundError(
                f"User with ID {user_id} was not found."
            )

        return user

    async def get_users(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> list[User]:
        return await self.repository.get_all(
            skip=skip,
            limit=limit,
        )

    async def update_user(
        self,
        user_id: int,
        user_data: UserUpdate,
    ) -> User:
        try:
            user = await self.repository.get_by_id(user_id)

            if user is None:
                raise UserNotFoundError(
                    f"User with ID {user_id} was not found."
                )

            # Extract only the fields provided by the client.
            update_data = user_data.model_dump(
                exclude_unset=True
            )

            # Check for duplicate email if the email is being changed.
            new_email = update_data.get("email")

            if new_email is not None and new_email != user.email:
                existing_user = await self.repository.get_by_email(
                    new_email
                )

                if existing_user:
                    raise EmailAlreadyRegisteredError(
                        "This email address is already registered."
                    )

            updated_user = await self.repository.update(
                user=user,
                update_data=update_data,
            )

            await self.db.commit()

            return updated_user

        except Exception:
            await self.db.rollback()
            raise

    async def authenticate_user(
    self,
    credentials: UserLogin,
    ) -> User | None:

        user = await self.repository.get_by_email(credentials.email)

        if not user:
            return None

        if not verify_password(
            credentials.password,
            user.password_hash,
        ):
            return None

        if not user.is_active:
            return None

        return user
