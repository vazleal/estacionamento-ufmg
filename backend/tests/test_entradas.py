import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_connection
import routes.entradas

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_dados():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM entradas")
        cursor.execute("DELETE FROM veiculos")
        cursor.execute("DELETE FROM usuarios")
        cursor.execute("DELETE FROM configuracoes WHERE id = 1")
        cursor.execute(
            "INSERT INTO configuracoes (id, total_vagas, reservadas_professores, aviso_limite) VALUES (1, 10, 4, 0.1)"
        )
        cursor.execute(
            "INSERT INTO usuarios (id, nome, email, senha, matricula, tipo) VALUES (1, 'Admin', 'admin@ex.com', 'admin', '000', 'admin')"
        )
        conn.commit()
    yield

ADMIN_HEADER = {"X-Usuario-Id": "1"}


def cadastrar_veiculo(usuario_id: int, placa: str, tipo: str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (id, nome, email, senha, matricula, tipo) VALUES (?, 'User', ?, 'x', 'm', ?)",
            (usuario_id, f"u{usuario_id}@ex.com", tipo),
        )
        cursor.execute(
            "INSERT INTO veiculos (usuario_id, placa) VALUES (?, ?)",
            (usuario_id, placa.upper()),
        )
        conn.commit()


def test_entrada_placa_nao_cadastrada():
    response = client.post("/entrada", json={"placa": "ABC1234"}, headers=ADMIN_HEADER)
    assert response.status_code == 404


def test_entrada_estacionamento_cheio(monkeypatch):
    cadastrar_veiculo(2, "XYZ1234", "aluno")

    class MockStats:
        livres = 0
        bloquear_aluno = False

    monkeypatch.setattr(routes.entradas, "get_estatisticas", lambda: MockStats())
    response = client.post("/entrada", json={"placa": "XYZ1234"}, headers=ADMIN_HEADER)
    assert response.status_code == 403


def test_entrada_aluno_bloqueado(monkeypatch):
    cadastrar_veiculo(2, "XYZ1234", "aluno")

    class MockStats:
        livres = 5
        bloquear_aluno = True

    monkeypatch.setattr(routes.entradas, "get_estatisticas", lambda: MockStats())
    response = client.post("/entrada", json={"placa": "XYZ1234"}, headers=ADMIN_HEADER)
    assert response.status_code == 403


def test_entrada_sucesso_professor(monkeypatch):
    cadastrar_veiculo(2, "PROF123", "professor")

    class MockStats:
        livres = 3
        bloquear_aluno = False

    monkeypatch.setattr(routes.entradas, "get_estatisticas", lambda: MockStats())
    response = client.post("/entrada", json={"placa": "PROF123"}, headers=ADMIN_HEADER)
    assert response.status_code == 200
    assert response.json()["status"] == "entrada registrada"


def test_saida_sem_entrada():
    cadastrar_veiculo(2, "SEM1234", "aluno")
    response = client.post("/saida", json={"placa": "SEM1234"}, headers=ADMIN_HEADER)
    assert response.status_code == 404
    assert "Nenhuma entrada" in response.json()["detail"]
