from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    email: str
    full_name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=12, max_length=72)


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
