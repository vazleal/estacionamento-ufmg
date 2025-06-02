import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_usuarios():
    from database import get_connection
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios")
        conn.commit()
    yield

def test_register_user_success():
    response = client.post("/register", json={
        "nome": "Teste",
        "email": "teste@example.com",
        "senha": "123456",
        "matricula": "abc123"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Teste"
    assert data["email"] == "teste@example.com"

def test_register_user_existing_email():
    client.post("/register", json={
        "nome": "Teste",
        "email": "teste2@example.com",
        "senha": "123456",
        "matricula": "abc123"
    })
    response = client.post("/register", json={
        "nome": "Teste",
        "email": "teste2@example.com",
        "senha": "123456",
        "matricula": "abc123"
    })
    assert response.status_code == 400

def test_login_success():
    client.post("/register", json={
        "nome": "Login Test",
        "email": "login@example.com",
        "senha": "senha123",
        "matricula": "mat123"
    })
    response = client.post("/login", json={
        "email": "login@example.com",
        "senha": "senha123"
    })
    assert response.status_code == 200
    assert "id" in response.json()

def test_login_wrong_password():
    client.post("/register", json={
        "nome": "Login Fail",
        "email": "fail@example.com",
        "senha": "senha123",
        "matricula": "mat123"
    })
    response = client.post("/login", json={
        "email": "fail@example.com",
        "senha": "errada"
    })
    assert response.status_code == 401
