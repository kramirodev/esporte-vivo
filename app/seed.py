from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_criar_usuario():
    response = client.post("/user/", json = {
        "telefone": "+5511999999999", 
        "nome": "João da Silva",
        "apelido": "joaosilva"})

    assert response.status_code == 201 or response.status_code == 200