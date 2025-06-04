import pytest
from fastapi.testclient import TestClient
from database import get_connection
from main import app

client = TestClient(app)

def test_put_config_invalid_data():
    payload = {"total_vagas": "cem", "reservadas_professores": 10, "aviso_limite": 0.1}
    response = client.put("/configuracoes", json=payload, headers={"X-Usuario-Id": "1"})
    assert response.status_code == 422
    json_data = response.json()
    assert "detail" in json_data
    assert any(error["loc"][-1] == "total_vagas" for error in json_data["detail"])

@pytest.fixture(autouse=True)
def reset_configuracoes():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM configuracoes WHERE id = 1")
        cursor.execute("""
            INSERT INTO configuracoes (id, total_vagas, reservadas_professores, aviso_limite)
            VALUES (1, 100, 40, 0.1)
        """)
        conn.commit()
    yield
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM configuracoes WHERE id = 1")
        conn.commit()

def test_obter_configuracoes():
    response = client.get("/configuracoes", headers={"X-Usuario-Id": "1"})
    assert response.status_code == 200
    json_data = response.json()
    assert json_data == {
        "total_vagas": 100,
        "reservadas_professores": 40,
        "aviso_limite": 0.1
    }

def test_atualizar_configuracoes():
    payload = {
        "total_vagas": 150,
        "reservadas_professores": 50,
        "aviso_limite": 0.2
    }
    response = client.put("/configuracoes", json=payload, headers={"X-Usuario-Id": "1"})
    assert response.status_code == 200
    assert response.json() == {"status": "configurações atualizadas"}

    # Verifica se os dados foram atualizados no banco
    response_get = client.get("/configuracoes", headers={"X-Usuario-Id": "1"})
    assert response_get.status_code == 200
    assert response_get.json() == payload

@pytest.mark.parametrize("payload,expected_status", [
    ({"total_vagas": "cem", "reservadas_professores": 10, "aviso_limite": 0.1}, 422),
    ({"total_vagas": 100, "reservadas_professores": None, "aviso_limite": 0.1}, 422),
])
def test_atualizar_configuracoes_dados_invalidos(payload, expected_status):
    response = client.put("/configuracoes", json=payload, headers={"X-Usuario-Id": "1"})
    assert response.status_code == expected_status
