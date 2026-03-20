from fastapi import status
from app.models.user import User

def test_list_users_empty(client):
  """Test retrieving user when the database is empty."""
  response = client.get("/user")
    
  assert response.status_code == status.HTTP_200_OK
  assert response.json() == []


def test_list_users_with_data(client, db_session):
  """Test retrieving a list containing multiple users."""
  user1 = User(name="Alice", email="alice@example.com")
  user2 = User(name="Bob", email="bob@example.com")
  db_session.add_all([user1, user2])
  db_session.commit()

  response = client.get("/user")
    
  assert response.status_code == status.HTTP_200_OK
  data = response.json()
  assert len(data) == 2
  assert data[0]["name"] == "Alice"
  assert data[1]["name"] == "Bob"

def test_create_user_with_data(client, db_session):
  """Test successful user creation via the POST /user/ endpoint."""
  payload = {
    "name": "Venkat Raman",
    "email": "venkat@example.com",
  }

  response = client.post("/user", json=payload)
  assert response.status_code == status.HTTP_201_CREATED
  data = response.json()
  assert data["name"] == "Venkat Raman"
  assert data["email"] == "venkat@example.com"
  assert "id" in data

  db_user = db_session.query(User).filter(User.email == "venkat@example.com").first()
  assert db_user is not None
  assert db_user.name == "Venkat Raman"


def test_get_user(client, db_session):
  """Test retrieving a specific user by ID."""
  new_user = User(name="Test User", email="findme@example.com")
  db_session.add(new_user)
  db_session.commit()
  db_session.refresh(new_user)

  response = client.get(f"/user/{new_user.id}")
  assert response.status_code == status.HTTP_200_OK

  data = response.json()
  assert data["id"] == new_user.id
  assert data["name"] == "Test User"

def test_delete_user_success(client, db_session):
  """Test successful deletion of a user."""
  user = User(name="To Be Deleted", email="delete@example.com")
  db_session.add(user)
  db_session.commit()
  user_id = user.id

  response = client.delete(f"/user/{user_id}")
  assert response.status_code == status.HTTP_200_OK
  assert response.json() is True

  deleted_user = db_session.query(User).filter(User.id == user_id).first()
  assert deleted_user is None

def test_update_user_success(client, db_session):
  """Test updating a user's name and email while leaving age unchanged."""
  user = User(name="Old Name", email="old@example.com")
  db_session.add(user)
  db_session.commit()
  db_session.refresh(user)

  payload = {
    "name": "New Name",
    "email": "new@example.com"
  }

  response = client.put(f"/user/{user.id}", json=payload)
  assert response.status_code == status.HTTP_200_OK

  data = response.json()
  
  assert data['name'] == payload["name"]
  assert data["email"] == "new@example.com"