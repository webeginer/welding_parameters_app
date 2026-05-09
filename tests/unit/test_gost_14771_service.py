import pytest
from backend.app.services.gost_14771_service import GOST14771Service


class TestGOST14771Service:
    
    def test_get_joint_groups(self):
        groups = GOST14771Service.get_joint_groups()
        group_codes = [g["code"] for g in groups]
        assert "C" in group_codes
        assert "У" in group_codes
        assert "Т" in group_codes
        assert "Н" in group_codes
    
    def test_get_joint_types(self):
        types = GOST14771Service.get_joint_types("C")
        codes = [t["code"] for t in types]
        assert "C1" in codes
        assert "C2" in codes
    
    def test_get_weld_processes(self):
        processes = GOST14771Service.get_weld_processes()
        codes = [p["code"] for p in processes]
        assert "ИН" in codes
        assert "ИНп" in codes
        assert "ИП" in codes
        assert "УП" in codes
    
    def test_get_constructive_elements_c1(self):
        elements = GOST14771Service.get_constructive_elements("C1", 2.0)
        assert "b" in elements
        assert "e" in elements
    
    def test_get_thickness_range(self):
        min_t, max_t = GOST14771Service.get_thickness_range("C1")
        assert min_t == 0.5
        assert max_t == 4.0
    
    def test_get_thickness_range_for_up(self):
        min_t, max_t = GOST14771Service.get_thickness_range("C1", process="УП")
        assert min_t == 0.5
        assert max_t == 60.0
