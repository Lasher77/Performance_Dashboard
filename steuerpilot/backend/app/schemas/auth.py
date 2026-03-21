from uuid import UUID

from pydantic import BaseModel

from app.models.user import UserRole


class RegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    role: UserRole = UserRole.MANDANT
    tenant_name: str = "Default"


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    role: UserRole
    tenant_id: UUID

    model_config = {"from_attributes": True}
