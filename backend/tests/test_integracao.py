import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_connection

@pytest.fixture(autouse=True)
def setup_and_cleanup_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        # Limpa e insere dados iniciais
        cursor.execute("DELETE FROM configuracoes")
        cursor.execute("INSERT INTO configuracoes (id, total_vagas, reservadas_professores, aviso_limite) VALUES (1, 100, 10, 0.2)")
        cursor.execute("DELETE FROM entradas")
        conn.commit()
    yield
    with get_connection() as conn:
        cursor = conn.cursor()
        # Limpa depois do teste para evitar interferência
        cursor.execute("DELETE FROM entradas")
        conn.commit()

client = TestClient(app)

def test_atualizar_configuracoes_api():
    # Define o payload com novos valores para atualização
    payload = {
        "total_vagas": 99,
        "reservadas_professores": 22,
        "aviso_limite": 0.3
    }
    # Envia uma requisição PUT para atualizar as configurações
    response = client.put("/configuracoes", json=payload)
    assert response.status_code == 200

    # Depois, faz um GET para verificar se os dados foram atualizados corretamente
    response_get = client.get("/configuracoes")
    data = response_get.json()
    assert data["total_vagas"] == 99
    assert data["reservadas_professores"] == 22
    # Compara com tolerância para valores float
    assert abs(data["aviso_limite"] - 0.3) < 0.01

def test_inserir_entrada_professor_api():
    # Obtém o número atual de professores registrados nas estatísticas
    response_before = client.get("/estatisticas")
    assert response_before.status_code == 200
    vagas_antes = response_before.json().get("professores", 0)

    # Registra uma nova entrada para professor via POST
    response_registro = client.post("/entrada/professor")
    assert response_registro.status_code == 200
    assert response_registro.json().get("status") == "entrada registrada"

    # Consulta as estatísticas novamente para verificar o aumento
    response_after = client.get("/estatisticas")
    assert response_after.status_code == 200
    vagas_depois = response_after.json().get("professores", 0)

    # Confirma que o número de professores aumentou em 1
    assert vagas_depois == vagas_antes + 1

def test_obter_configuracoes_api():
    # Faz uma requisição GET para a rota /configuracoes
    response = client.get("/configuracoes")  

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, dict)

    assert "total_vagas" in data and data["total_vagas"] > 0
    # Verifica se a chave 'reservadas_professores' existe e é um inteiro
    assert "reservadas_professores" in data and isinstance(data["reservadas_professores"], int)
