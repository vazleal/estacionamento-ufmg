from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user_success():
    response = client.post("/register", json={
        "nome": "Teste",
        "email": "teste@example.com",
        "senha": "123456",
        "matricula": "abc123",
        "tipo": "aluno"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == "Teste"
    assert data["email"] == "teste@example.com"
    assert data["tipo"] == "aluno"

def test_register_user_existing_email():
    client.post("/register", json={
        "nome": "Teste",
        "email": "teste2@example.com",
        "senha": "123456",
        "matricula": "abc123",
        "tipo": "aluno"
    })
    response = client.post("/register", json={
        "nome": "Teste",
        "email": "teste2@example.com",
        "senha": "123456",
        "matricula": "abc123",
        "tipo": "aluno"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Usuário já existe"}

def test_login_success():
    client.post("/register", json={
        "nome": "Login Test",
        "email": "login@example.com",
        "senha": "senha123",
        "matricula": "mat123",
        "tipo": "professor"
    })
    response = client.post("/login", json={
        "email": "login@example.com",
        "senha": "senha123"
    })
    assert response.status_code == 200
    assert response.json()["tipo"] == "professor"

def test_login_wrong_password():
    client.post("/register", json={
        "nome": "Login Fail",
        "email": "fail@example.com",
        "senha": "senha123",
        "matricula": "mat123",
        "tipo": "aluno"
    })
    response = client.post("/login", json={
        "email": "fail@example.com",
        "senha": "errada"
    })
    assert response.status_code == 401, response.text
    assert response.json()["detail"] == "Credenciais inválidas"
    
def test_login_non_existing_user():
    response = client.post("/login", json={
        "email": "naoexiste@example.com",
        "senha": "qualquercoisa"
    })
    assert response.status_code == 401, response.text 
    assert response.json()["detail"] == "Credenciais inválidas"
