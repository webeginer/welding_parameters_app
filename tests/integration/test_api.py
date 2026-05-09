import pytest
from fastapi.testclient import TestClient


class TestAPI:
    """Тесты API эндпоинтов"""
    
    def test_calculate_rds_endpoint(self, client: TestClient, sample_rds_request):
        """Тест эндпоинта /api/calculate для РДС"""
        response = client.post("/api/calculate", json=sample_rds_request.model_dump())
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "parameters" in data
    
    def test_calculate_tig_aluminum_endpoint(self, client: TestClient, sample_tig_aluminum_request):
        """Тест эндпоинта /api/calculate для TIG + Алюминий (ГОСТ 14806-80)"""
        response = client.post("/api/calculate", json=sample_tig_aluminum_request.model_dump())
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
    
    def test_calculate_mig_endpoint(self, client: TestClient, sample_mig_request):
        """Тест эндпоинта /api/calculate для MIG-MAG"""
        response = client.post("/api/calculate", json=sample_mig_request.model_dump())
        
        assert response.status_code == 200
        assert response.json()["success"] is True
    
    def test_get_joint_groups_endpoint(self, client: TestClient):
        """Тест получения групп соединений"""
        response = client.get("/api/gost/joint-groups?gost=ГОСТ 14806-80")
        
        assert response.status_code == 200
        data = response.json()
        assert "groups" in data
    
    def test_get_joint_types_endpoint(self, client: TestClient):
        """Тест получения типов соединений по группе"""
        response = client.get("/api/gost/joint-types?gost=ГОСТ%2014806-80&group=C")
        
        assert response.status_code == 200
        data = response.json()
        assert "types" in data
        assert any(t["code"] == "C1" for t in data["types"])
    
    def test_invalid_method_error(self, client: TestClient):
        """Тест обработки ошибки: неверный метод сварки"""
        response = client.post("/api/calculate", json={
            "method": "INVALID",
            "thickness": 4.0
        })
        
        assert response.status_code == 422
    
    def test_thickness_out_of_range_error(self, client: TestClient):
        """Тест обработки ошибки: толщина вне диапазона ГОСТ"""
        response = client.post("/api/calculate", json={
            "method": "TIG",
            "material": "ALUMINUM",
            "thickness": 100.0,
            "joint_group": "C",
            "joint_type": "C4",
            "length": 500,
            "position": "lower"
        })
        
        assert response.status_code == 422
