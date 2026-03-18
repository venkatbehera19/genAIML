from app.schemas.user_schema import User, Updateuser, CreateUser

class UserService:
  """This Service is used manage user operations.

  It Provide in-memeory CRUD(Create, Edit, Update, Delete)
  functionality for user objects. It simulates a data store
  using list and auto increments user id.

  Attributes:
  users: List storing all the user object.
  counter: auto incrementing id for new users.
  
  """
  def __init__(self):
    """
    Initializes the instance with default value of
    users as empty list[] and counters as 1 
    """
    self.users = []
    self.counter = 1

  async def create_user(self, user: CreateUser):
    """Add the user object to the users.

    Args:
      user: A CreateUser schema object containing the
        name, age, and email of the user to be created

    Returns:
      User: The newly created User object with its assigned ID.
    """
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
    """list all the user object

    Args:
      no arguments required
    Returns:
      list [User]: return all the user object that present inside users list.
    """
    return self.users
  
  async def get_user(self, user_id: int):
    """Retrieve a user from the collection by their ID.

    Args:
      user_id: The unique integer ID of the user to find.

    Returns:
      User: the user object is found, otherwise none.
    """
    for user in self.users:
      if user.id == user_id:
        return user
      
    return None
  
  async def update_user(self, user_id: int, data: Updateuser):
    """Update the existing user details based on provided data.

    Args:
      user_id: The unique integer ID of the user to find.
      data: An Updateuser object containing the optional fields to be updated.

    Returns:
      User: the updated user object if the ID was found, otherwise none.
    """
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
    """Remove a user from the collection by their ID.

    Args:
      user_id: The unique integer ID of the user to find.

    Returns:
      bool: True if the user was found and removed, false otherwise

    """
    for user in self.users:
      if user.id == user_id:
        self.users.remove(user)
        return True
      
    return False