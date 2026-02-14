from pydantic import BaseModel, EmailStr

class RegisterIn(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class CourseCreate(BaseModel):
    title: str
    description: str | None = None

class CourseOut(BaseModel):
    id: int
    title: str
    description: str | None = None

    class Config:
        from_attributes = True
