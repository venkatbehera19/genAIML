from app.services.user_service import UserService

user_service = UserService()

def get_user_services():
  return user_service