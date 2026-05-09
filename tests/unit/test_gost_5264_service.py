import pytest
from backend.app.services.gost_5264_service import GOST5264Service


class TestGOST5264Service:
    
    def test_get_joint_groups(self):
        groups = GOST5264Service.get_joint_groups()
        group_codes = [g["code"] for g in groups]
        assert "C" in group_codes
        assert "У" in group_codes
        assert "Т" in group_codes
        assert "Н" in group_codes
    
    def test_get_joint_types_for_group_c(self):
        types = GOST5264Service.get_joint_types("C")
        codes = [t["code"] for t in types]
        assert "C1" in codes
        assert "C2" in codes
    
    def test_get_joint_types_for_group_invalid(self):
        types = GOST5264Service.get_joint_types("X")
        assert types == []
    
    def test_get_constructive_elements_c1(self):
        elements = GOST5264Service.get_constructive_elements("C1", 3.0)
        assert elements["b"] == 0
        assert elements["e"] is not None
    
    def test_get_constructive_elements_c2(self):
        elements = GOST5264Service.get_constructive_elements("C2", 2.0)
        assert elements["b"] == 1
        assert elements["e"] == 7
        assert elements["g"] == 1.5
    
    def test_get_thickness_range(self):
        min_t, max_t = GOST5264Service.get_thickness_range("C1")
        assert min_t == 1
        assert max_t == 4
    
    def test_get_thickness_range_default(self):
        min_t, max_t = GOST5264Service.get_thickness_range("UNKNOWN")
        assert min_t == 1
        assert max_t == 60
    
    def test_calculate_Fn_butt(self):
        elements = {"b": 2, "e": 8, "g": 2}
        Fn = GOST5264Service.calculate_Fn("C2", 4.0, elements)
        assert Fn > 0
