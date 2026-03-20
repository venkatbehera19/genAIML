def test_calculate_tax_success(client):
  """Test successful tax calculation with valid data."""
  payload = {
    "basic": 500000,
    "hra": 200000,
    "other_allowances": 100000,
    "tax_regime": "new"
  }
    
  response = client.post("/tax/", json=payload)
  assert response.status_code == 200