import pytest
from unittest.mock import Mock
from app import app, reset_inventory

@pytest.fixture
def client():
    reset_inventory()
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def test_list_empty(client):
    r = client.get('/items')
    assert r.status_code == 200
    assert r.get_json() == []

def test_create_and_get(client):
    r = client.post('/items', json={'name': 'Test', 'quantity': 3})
    assert r.status_code == 201
    data = r.get_json()
    assert data['id'] == 1
    assert data['name'] == 'Test'

    r2 = client.get('/items/1')
    assert r2.status_code == 200
    assert r2.get_json()['quantity'] == 3

def test_update(client):
    client.post('/items', json={'name': 'Old', 'quantity': 1})
    r = client.patch('/items/1', json={'name': 'New', 'price': 9.99})
    assert r.status_code == 200
    data = r.get_json()
    assert data['name'] == 'New'
    assert data['price'] == 9.99

def test_delete(client):
    client.post('/items', json={'name': 'Delete me'})
    r = client.delete('/items/1')
    assert r.status_code == 204
    assert client.get('/items').get_json() == []

def test_external_barcode_mock(client, monkeypatch):
    def fake_get(*args, **kwargs):
        m = Mock()
        m.status_code = 200
        m.json.return_value = {
            'status': 1,
            'product': {
                'product_name': 'Mock Product',
                'brands': 'Mock Brand',
                'categories': 'Cat',
                'ingredients_text': 'ingredients'
            }
        }
        return m
    monkeypatch.setattr('app.requests.get', fake_get)
    r = client.get('/external/barcode/123')
    assert r.status_code == 200
    data = r.get_json()
    assert data['name'] == 'Mock Product'
    assert data['barcode'] == '123'

def test_add_external_mock(client, monkeypatch):
    def fake_get(*args, **kwargs):
        m = Mock()
        m.status_code = 200
        m.json.return_value = {
            'status': 1,
            'product': {
                'product_name': 'External Item',
                'brands': 'Brand X',
                'categories': '',
                'ingredients_text': ''
            }
        }
        return m
    monkeypatch.setattr('app.requests.get', fake_get)
    r = client.post('/external/add/999', json={'quantity': 2, 'price': 5.0})
    assert r.status_code == 201
    data = r.get_json()
    assert data['name'] == 'External Item'
    assert data['quantity'] == 2
