import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_obter_configuracoes_api():
    # Faz uma requisição GET para a rota /configuracoes
    response = client.get("/configuracoes")  
    # Verifica se a resposta foi bem-sucedida
    assert response.status_code == 200
    data = response.json()
    # Confirma que o retorno é um dicionário
    assert isinstance(data, dict)
    # Verifica se a chave 'total_vagas' existe e tem valor positivo
    assert "total_vagas" in data and data["total_vagas"] > 0
    # Verifica se a chave 'reservadas_professores' existe e é um inteiro
    assert "reservadas_professores" in data and isinstance(data["reservadas_professores"], int)

