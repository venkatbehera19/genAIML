from app.schemas.user_schema import User, Updateuser, CreateUser

class UserService:
  def __init__(self):
    self.users = []
    self.counter = 1

  async def create_user(self, user: CreateUser):

    new_user = User(
      id= self.counter,
      name= user.name,
      age= user.age,
      email= user.email
    )

    self.users.append(new_user)
    self.counter += 1

    return new_user
  
  async def list_user(self):

    return self.users
  
  async def get_user(self, user_id: int):

    for user in self.users:
      if user.id == user_id:
        return user
      
    return None
  
  async def update_user(self, user_id: int, data: Updateuser):

    for user in self.users:

      if user.id == user_id:

        if data.name:
          user.name = data.name
        if data.age:
          user.age = data.age
        if data.email:
          user.email = data.email

        return user
      
    return None
  
  async def delete_user(self, user_id: int):

    for user in self.users:
      if user.id == user_id:
        self.users.remove(user)
        return True
      
    return False