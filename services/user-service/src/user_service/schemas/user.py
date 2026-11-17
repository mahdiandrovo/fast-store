from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone_number: str | None = Field(default=None, max_length=20)
    country: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=8, max_length=128)

class UserUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    email: EmailStr | None = None
    phone_number: str | None = Field(default=None, max_length=20)
    country: str | None = Field(default=None, min_length=2, max_length=100)

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    phone_number: str | None
    country: str
    is_active: bool
