import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_connection
import routes.entradas

client = TestClient(app)

# Reset entradas e configuracoes para cada teste
@pytest.fixture(autouse=True)
def reset_dados():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entradas")
        cursor.execute("DELETE FROM configuracoes WHERE id = 1")
        cursor.execute("""
            INSERT INTO configuracoes (id, total_vagas, reservadas_professores, aviso_limite)
            VALUES (1, 10, 4, 0.1)
        """)
        conn.commit()
    yield


#TESTES 
def test_entrada_tipo_invalido():
    response = client.post("/entrada/invalido", json={"placa": "ABC1234"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Tipo inválido"

def test_saida_tipo_invalido():
    response = client.post("/saida/invalido", json={"placa": "ABC1234"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Tipo inválido"

def test_entrada_estacionamento_cheio(monkeypatch):
    class MockStats:
        livres = 0
        bloquear_aluno = False

    monkeypatch.setattr(routes.entradas, "get_estatisticas", lambda: MockStats())

    response = client.post("/entrada/aluno", json={"placa": "XYZ1234"})
    assert response.status_code == 403

def test_entrada_aluno_bloqueado(monkeypatch):
    class MockStats:
        livres = 5
        bloquear_aluno = True

    monkeypatch.setattr(routes.entradas, "get_estatisticas", lambda: MockStats())

    response = client.post("/entrada/aluno", json={"placa": "XYZ1234"})
    assert response.status_code == 403

def test_entrada_sucesso_professor(monkeypatch):
    class MockStats:
        livres = 3
        bloquear_aluno = False

    monkeypatch.setattr(routes.entradas, "get_estatisticas", lambda: MockStats())

    response = client.post("/entrada/professor", json={"placa": "PROF123"})
    assert response.status_code == 200
    assert response.json() == {"status": "entrada registrada"}

def test_saida_sem_entrada():
    response = client.post("/saida/aluno", json={"placa": "SEM1234"})
    assert response.status_code == 404
    assert "Nenhuma entrada de aluno" in response.json()["detail"]
    