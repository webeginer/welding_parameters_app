import pytest
from backend.app.services.gost_14806_service import GOST14806Service
from backend.app.models import WeldProcess


class TestGOST14806Service:
    """Тесты для ГОСТ 14806-80"""
    
    @pytest.fixture
    def gost_service(self, test_db):
        """Фикстура для сервиса ГОСТ"""
        return GOST14806Service(test_db)
    
    def test_get_joint_groups(self, gost_service):
        """Тест получения групп соединений"""
        groups = gost_service.get_joint_groups()
        
        # Проверяем наличие всех групп
        group_codes = [g["code"] for g in groups]
        assert "C" in group_codes
        assert "У" in group_codes
        assert "Т" in group_codes
        assert "Н" in group_codes
    
    def test_get_joint_types_by_group(self, gost_service):
        """Тест получения типов соединений по группе"""
        # Стыковые соединения
        c_types = gost_service.get_joint_types_by_group("C")
        c_codes = [t["code"] for t in c_types]
        
        assert "C1" in c_codes
        assert "C4" in c_codes
        assert "C44" in c_codes
        
        # Угловые соединения
        u_types = gost_service.get_joint_types_by_group("У")
        u_codes = [t["code"] for t in u_types]
        
        assert "У1" in u_codes
        assert "У4" in u_codes
        assert "У14" in u_codes
    
    def test_get_constructive_elements_c4(self, gost_service):
        """Тест получения конструктивных элементов для C4 (табл.5)"""
        elements = gost_service.get_constructive_elements(
            joint_type="C4",
            thickness=8.0,
            process=WeldProcess.AINP
        )
        
        assert elements["b"] == 16
        assert elements["e"] == 19
        assert elements["g"] == 2.0
    
    def test_get_constructive_elements_c7(self, gost_service):
        """Тест получения конструктивных элементов для C7 (табл.7)"""
        elements = gost_service.get_constructive_elements(
            joint_type="C7",
            thickness=5.0,
            process=WeldProcess.RINP
        )
        
        assert elements["b"] == 16
        assert elements["R"] == 2
    
    def test_get_constructive_elements_t1(self, gost_service):
        """Тест получения конструктивных элементов для T1 (табл.42)"""
        elements = gost_service.get_constructive_elements(
            joint_type="T1",
            thickness=4.0,
            process=WeldProcess.RINP
        )
        
        assert elements["K"] == 3
    
    def test_validate_thickness(self, gost_service):
        """Тест валидации толщины для типа соединения"""
        assert gost_service.validate_thickness(
            joint_type="C4",
            thickness=8.0,
            process=WeldProcess.AINP
        ) is True
        
        assert gost_service.validate_thickness(
            joint_type="C4",
            thickness=12.0,
            process=WeldProcess.AINP
        ) is False
    
    def test_get_available_processes(self, gost_service):
        """Тест получения доступных способов сварки для типа соединения"""
        processes = gost_service.get_available_processes("C4")
        
        assert "РИНп" in processes
        assert "АИНп" in processes
        assert "АИНп-3" in processes
        assert "АИП" in processes
        assert "ПИП" in processes
    
    def test_calculate_Fn_c4(self, gost_service):
        """Тест расчёта площади шва для C4"""
        thickness = 8.0
        elements = {
            "b": 16,
            "e": 19,
            "g": 2.0
        }
        
        Fn = gost_service.calculate_Fn(
            joint_type="C4",
            thickness=thickness,
            elements=elements
        )
        
        expected = (thickness * elements["b"] + 0.75 * elements["e"] * elements["g"]) / 100
        assert abs(Fn - expected) < 0.01
    
    def test_get_tables_range_c4(self, gost_service):
        """Тест получения диапазона таблиц для C4"""
        tables = gost_service.get_applicable_tables("C4")
        
        assert "табл.4" in tables
        assert "табл.5" in tables
        assert "табл.6" in tables
