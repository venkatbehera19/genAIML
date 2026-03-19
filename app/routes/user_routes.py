from fastapi import APIRouter, Depends, status, HTTPException

from app.schemas.user_schema import Updateuser, CreateUser, User as UserBase
from app.config.log_config import logger
from app.db.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.user import User

from app.exceptions import NotFoundError, InternalServerError

router = APIRouter(prefix="/user", tags=["user"])

@router.get('/', response_model=list[UserBase], status_code= status.HTTP_200_OK)
async def list_users(db: Session= Depends(get_db)):
  """Retrive a list of all users

  Returns:
    list[UserBase]: a list containing of all user records.
  """
  try:
    users =  db.query(User).all()
    return users
  
  except SQLAlchemyError as e:
    logger.error("Database error during user fetch: ", str(e))
    raise InternalServerError("A database error occurred while creating users.") from e
  
  except Exception as e:
    db.rollback()
    logger.error("Unexpected error in list_users:", str(e))
    raise InternalServerError("A database error occurred while creating users.") from e

@router.post('/', status_code= status.HTTP_201_CREATED)
async def create_user(user: CreateUser ,db: Session= Depends(get_db)):
  """Create a new user

  Args:
    user: A CreateUser schema object containing the
      name, age, and email of the user to be created

  Returns:
    User: The newly created user object including its generated ID.
  """
  try:
    new_user = User(
      name = user.name,
      email = user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
  
  except SQLAlchemyError as e:
    db.rollback()
    logger.error("Database error during user fetch: ", str(e))
    raise InternalServerError("A database error occurred while retrieving users.") from e
  
  except Exception as e:
    db.rollback()
    logger.error("Unexpected error in list_users:", str(e))
    raise InternalServerError("An unexpected internal server error occurred.") from e

@router.get('/{user_id}')
async def get_user(user_id: int, db: Session= Depends(get_db)):
  """Get a specific user by their ID.

  Args: 
    user_id: The unique identifier of the user.

  Returns:
    User: The requested user object.
  """
  try:
    user = db.get(User, user_id)
    return user
  except SQLAlchemyError as e:
    db.rollback()
    logger.error("Database error during user fetch: ", str(e))
    raise InternalServerError("A database error occurred while retrieving users.") from e
  
  except Exception as e:
    db.rollback()
    logger.error("Unexpected error in list_users:", str(e))
    raise InternalServerError("An unexpected internal server error occurred.") from e
  

@router.delete('/{user_id}', response_model=bool)
async def delete_user(user_id: int, db: Session= Depends(get_db)):
  """Delete a specific user by their ID.

  Args:
    user_id: The unique identifier of the user.

  Returns:
    bool: True if the deletion was successful. otherwise false
  """
  user_to_delete = db.query(User).filter(User.id == user_id).first()
  if not user_to_delete:
    raise NotFoundError(f"User with id {user_id} does not exist")
  
  try:
    db.delete(user_to_delete)
    db.commit()
    return True

  except SQLAlchemyError as e:
    db.rollback()
    logger.error("Database error during deleting user ", str(e))
    raise InternalServerError("A database error occurred while retrieving users.") from e
  
  except Exception as e:
    db.rollback()
    logger.error("Error deleting user:", str(e))
    raise InternalServerError("A database error occurred while retrieving users.") from e
  

@router.put('/{user_id}')
async def update_user(user_id: int, user_data: Updateuser, db: Session= Depends(get_db)):
  """Update an existing user's information.

  Args:
    user_id: The unique identifier of the user.
    user_data: An Updateuser object containing the optional fields to be updated.

  Returns:
    User: the updated user object if the ID was found, otherwise none.
  """
  db_user = db.query(User).filter(User.id == user_id).first()

  if not db_user:
    raise NotFoundError(f"User with id {user_id} does not exist")
  
  try:
    updated_data = user_data.model_dump(exclude_unset=True)

    for key, value in updated_data.items():
      if hasattr(db_user, key): 
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user

  except SQLAlchemyError as e:
    db.rollback()
    logger.error("Database error during deleting user ", str(e))
    raise InternalServerError("A database error occurred while deleting users.") from e
  
  except Exception as e:
    db.rollback()
    logger.error("Error deleting user:", str(e))
    raise InternalServerError("A database error occurred while deleting users.") from e