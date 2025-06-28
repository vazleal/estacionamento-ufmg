import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_connection

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_cleanup_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        # Limpa e insere dados iniciais
        cursor.execute("DELETE FROM configuracoes")
        cursor.execute(
            "INSERT INTO configuracoes (id, total_vagas, reservadas_professores, aviso_limite) VALUES (1, 100, 10, 0.2)"
        )
        cursor.execute("DELETE FROM entradas")
        cursor.execute("DELETE FROM usuarios")
        cursor.execute("DELETE FROM veiculos")
        conn.commit()
    yield
    with get_connection() as conn:
        cursor = conn.cursor()
        # Limpa depois do teste para evitar interferência
        cursor.execute("DELETE FROM entradas")
        cursor.execute("DELETE FROM usuarios")
        cursor.execute("DELETE FROM veiculos")
        conn.commit()

@pytest.fixture
def admin_user_headers():
    resp = client.post("/register", json={
        "nome": "Admin Teste",
        "email": "admin@example.com",
        "senha": "123456",
        "matricula": "adm123",
        "tipo": "admin"
    })
    assert resp.status_code == 200
    user_id = resp.json()["id"]
    return {"x-usuario-id": str(user_id)}

@pytest.fixture
def professor_user_with_vehicle(admin_user_headers):
    resp_user = client.post("/register", json={
        "nome": "Professor Teste",
        "email": "professor@example.com",
        "senha": "123456",
        "matricula": "prof123",
        "tipo": "professor"
    })
    assert resp_user.status_code == 200
    user_id = resp_user.json()["id"]

    resp_veiculo = client.post(f"/usuario/{user_id}/veiculos", json={"placa": "PROF123"}, headers=admin_user_headers)
    assert resp_veiculo.status_code == 200

    return {
        "user_id": user_id,
        "placa": "PROF123"
    }

def test_obter_configuracoes_api(admin_user_headers):
    response = client.get("/configuracoes", headers=admin_user_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "total_vagas" in data and data["total_vagas"] > 0
    assert "reservadas_professores" in data and isinstance(data["reservadas_professores"], int)

def test_inserir_entrada_professor_api(professor_user_with_vehicle, admin_user_headers):
    response_before = client.get("/estatisticas", headers=admin_user_headers)
    assert response_before.status_code == 200
    vagas_antes = response_before.json().get("professores", 0)

    response_registro = client.post("/entrada", json={"placa": professor_user_with_vehicle["placa"]}, headers=admin_user_headers)
    assert response_registro.status_code == 200
    assert response_registro.json().get("status") == "entrada registrada"

    response_after = client.get("/estatisticas", headers=admin_user_headers)
    assert response_after.status_code == 200
    vagas_depois = response_after.json().get("professores", 0)

    assert vagas_depois == vagas_antes + 1

def test_atualizar_configuracoes_api(admin_user_headers):
    payload = {
        "total_vagas": 99,
        "reservadas_professores": 22,
        "aviso_limite": 0.3
    }
    response = client.put("/configuracoes", json=payload, headers=admin_user_headers)
    assert response.status_code == 200

    response_get = client.get("/configuracoes", headers=admin_user_headers)
    assert response_get.status_code == 200
    data = response_get.json()
    assert data["total_vagas"] == 99
    assert data["reservadas_professores"] == 22
    assert abs(data["aviso_limite"] - 0.3) < 0.01

def test_acesso_sem_autenticacao_negado():
    response = client.get("/configuracoes")
    assert response.status_code == 401
    response = client.post("/entrada", json={"placa": "QUALQUER"})
    assert response.status_code == 401
