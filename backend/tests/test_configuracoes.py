import pytest
from fastapi.testclient import TestClient
from database import get_connection
from main import app

client = TestClient(app)

def test_put_config_invalid_data():
    payload = {"total_vagas": "cem", "reservadas_professores": 10, "aviso_limite": 0.1}
    response = client.put("/configuracoes", json=payload)
    assert response.status_code == 422
    json_data = response.json()
    assert "detail" in json_data
    assert any(error["loc"][-1] == "total_vagas" for error in json_data["detail"])




