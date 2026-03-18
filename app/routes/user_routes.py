from fastapi import APIRouter, Depends, status

from app.schemas.user_schema import User, Updateuser, CreateUser
from app.services.user_service import UserService
from app.dependencies.user import get_user_services
from app.config.log_config import logger

router = APIRouter(prefix="/user", tags=["user"])

@router.get('/', response_model=list[User])
async def list_users(service: UserService = Depends(get_user_services)):
  """Retrive a list of all users

  Returns:
    list[User]: a list containing of all user records.
  """
  return await service.list_user()

@router.post('/', response_model=User, status_code= status.HTTP_201_CREATED)
async def create_user(user: CreateUser ,service: UserService = Depends(get_user_services)):
  """Create a new user

  Args:
    user: A CreateUser schema object containing the
      name, age, and email of the user to be created

  Returns:
    User: The newly created user object including its generated ID.
  """
  return await service.create_user(user)

@router.get('/{user_id}', response_model=User)
async def get_user(user_id: int, service: UserService = Depends(get_user_services)):
  """Get a specific user by their ID.

  Args: 
    user_id: The unique identifier of the user.

  Returns:
    User: The requested user object.
  """
  return await service.get_user(user_id)

@router.delete('/{user_id}', response_model=bool)
async def delete_user(user_id: int, service: UserService = Depends(get_user_services)):
  """Delete a specific user by their ID.

  Args:
    user_id: The unique identifier of the user.

  Returns:
    bool: True if the deletion was successful. otherwise false
  """
  return await service.delete_user(user_id)

@router.put('/{user_id}', response_model=User)
async def update_user(user_id: int, user_data: Updateuser, service: UserService = Depends(get_user_services)):
  """Update an existing user's information.

  Args:
    user_id: The unique identifier of the user.
    user_data: An Updateuser object containing the optional fields to be updated.

  Returns:
    User: the updated user object if the ID was found, otherwise none.
  """
  return await service.update_user(user_id, user_data)