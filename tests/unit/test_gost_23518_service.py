import pytest
from backend.app.services.gost_23518_service import GOST23518Service


class TestGOST23518Service:
    
    def test_get_joint_groups(self):
        groups = GOST23518Service.get_joint_groups()
        group_codes = [g["code"] for g in groups]
        assert "У" in group_codes
        assert "Т" in group_codes
        assert "C" not in group_codes
    
    def test_get_joint_types(self):
        types = GOST23518Service.get_joint_types("У")
        codes = [t["code"] for t in types]
        assert "У1" in codes
    
    def test_get_weld_processes(self):
        processes = GOST23518Service.get_weld_processes()
        codes = [p["code"] for p in processes]
        assert "ИН" in codes
        assert "УП" in codes
    
    def test_get_constructive_elements(self):
        elements = GOST23518Service.get_constructive_elements("У1", 2.0)
        assert "b" in elements
        assert "e" in elements
        assert elements["β"] == 90
    
    def test_get_thickness_range(self):
        min_t, max_t = GOST23518Service.get_thickness_range("У1")
        assert min_t == 0.5
        assert max_t == 4.0
    
    def test_get_angle_range(self):
        min_a, max_a = GOST23518Service.get_angle_range("Т1")
        assert min_a == 91
        assert max_a == 175
