import pytest
from app import app, mock_db, Product

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_all_products(client):
    response = client.get('/product')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_single_product(client):
    response = client.get('/product/1')
    assert response.status_code == 200
    assert response.json['name'] == "Organic Almond Milk"

def test_update_product(client):
    response = client.patch('/product/1', json={"name": "Updated Milk"})
    assert response.status_code == 200
    assert response.json['name'] == "Updated Milk"

def test_delete_product(client):
    # Make sure we have a product to delete first
    mock_db.append(Product(99, "Delete Me", "000", "Brand", "Ingredients"))
    response = client.delete('/product/99')
    assert response.status_code == 204
    
def test_delete_nonexistent_product(client):
    response = client.delete('/product/9999')
    assert response.status_code == 404