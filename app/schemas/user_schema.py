from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
  id: int
  name: str
  age: int
  email: EmailStr

class CreateUser(BaseModel):
  email: EmailStr
  age: int
  name: str

class Updateuser(BaseModel):
  name: Optional[str] = None
  email: Optional[EmailStr] = None
  age: Optional[int] = None