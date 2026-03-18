from fastapi import APIRouter, Depends, status

from app.schemas.user_schema import User, Updateuser, CreateUser
from app.services.user_service import UserService
from app.dependencies.user import get_user_services
from app.core.logger import logger

router = APIRouter(prefix="/user", tags=["user"])

@router.get('/', response_model=list[User])
async def list_users(service: UserService = Depends(get_user_services)):
  return await service.list_user()

@router.post('/', response_model=User, status_code= status.HTTP_201_CREATED)
async def create_user(user: CreateUser ,service: UserService = Depends(get_user_services)):
  return await service.create_user(user)

@router.get('/{user_id}', response_model=User)
async def get_user(user_id: int, service: UserService = Depends(get_user_services)):
  return await service.get_user(user_id)

@router.delete('/{user_id}', response_model=bool)
async def delete_user(user_id: int, service: UserService = Depends(get_user_services)):
  return await service.delete_user(user_id)

@router.put('/{user_id}', response_model=User)
async def update_user(user_id: int, user_data: Updateuser, service: UserService = Depends(get_user_services)):
  return await service.update_user(user_id, user_data)