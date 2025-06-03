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
    response = client.post("/entrada/invalido")
    assert response.status_code == 400
    assert response.json()["detail"] == "Tipo inválido"

