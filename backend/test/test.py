import pytest
from fastapi.testclient import TestClient
import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_health_check():
    """Testa se a API está online"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_chat_flow():
    """Testa o fluxo completo do chat"""
    response = client.post("/prepare-db")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"