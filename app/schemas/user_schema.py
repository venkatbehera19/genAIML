from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class BaseUser(BaseModel):
  """Base attributes shared across create and update schemas."""
  name: str
  email: EmailStr

class CreateUser(BaseUser):
  """Schema for creating the user"""
  pass

class Updateuser(BaseUser):
  """Schema for updating a user; all fields are optional."""
  name: Optional[str] = None
  email: Optional[EmailStr] = None

class User(BaseUser):
  """Schema for returning a user, including the database ID."""
  id: int
  model_config = ConfigDict(from_attributes=True)