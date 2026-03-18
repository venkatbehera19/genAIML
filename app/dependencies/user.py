from app.services.user_service import UserService

# Global instance of the service (Singleton pattern)
user_service = UserService()

def get_user_services():
  """
  Provide a singleton instance of UserService for dependency injection.

  This function is intended to be used with FastAPI's `Depends` to ensure 
  that routes have access to the user management logic.

  Returns:
    UserService: A shared instance of the user service.
  """
  return user_service