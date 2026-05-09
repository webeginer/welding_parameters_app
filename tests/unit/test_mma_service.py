import pytest
from backend.app.services.mma_service import MMAService
from backend.app.models import CalculationRequest, WeldMethod, Material


class TestMMAService:
    """Тесты для MMA сервиса"""
    
    def test_electrode_diameter_by_thickness(self):
        assert MMAService.get_electrode_diameter(1.5) == 1.6
        assert MMAService.get_electrode_diameter(2.5) == 2.5
        assert MMAService.get_electrode_diameter(4.0) == 3.0
        assert MMAService.get_electrode_diameter(8.0) == 4.0
        assert MMAService.get_electrode_diameter(12.0) == 5.0
        assert MMAService.get_electrode_diameter(20.0) == 6.0
    
    def test_k_coefficient(self):
        assert MMAService.get_k_coefficient(1.6) == 27.5
        assert MMAService.get_k_coefficient(3.0) == 37.5
        assert MMAService.get_k_coefficient(5.0) == 52.5
    
    def test_current_calculation(self):
        current = MMAService.calculate_current(4.0)
        # 37.5 * 4 = 150
        assert current == 150.0
    
    def test_current_correction_vertical(self):
        current = MMAService.correct_current(150, "vertical")
        assert current == 135.0
    
    def test_current_correction_ceiling(self):
        current = MMAService.correct_current(150, "ceiling")
        assert current == 127.5
    
    def test_current_correction_lower(self):
        current = MMAService.correct_current(150, "lower")
        assert current == 150.0
    
    def test_welding_speed(self):
        speed = MMAService.calculate_welding_speed(150)
        assert speed == 9.5  # 8 + (50 * 0.03)
    
    def test_calculate(self):
        request = CalculationRequest(
            method=WeldMethod.MMA,
            material=Material.CARBON_STEEL,
            thickness=8.0,
            joint_group="C",
            joint_type="C1",
            length=500,
            position="lower",
            electrode_brand="УОНИ 13/45"
        )
        
        result = MMAService.calculate(request)
        
        assert result["electrode_diameter"] == 4.0
        assert 140 <= result["current"] <= 160
        assert result["voltage"] == 25.0
        assert result["polarity"] == "Постоянный или переменный ток"
        assert result["electrode_brand"] == "УОНИ 13/45"
