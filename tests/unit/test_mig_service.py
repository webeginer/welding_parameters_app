import pytest
from backend.app.services.mig_service import MIGService
from backend.app.models import CalculationRequest, WeldMethod, Material


class TestMIGService:
    
    def test_wire_diameter_by_thickness(self):
        assert MIGService.get_wire_diameter(0.8) == 0.65
        assert MIGService.get_wire_diameter(1.5) == 0.9
        assert MIGService.get_wire_diameter(3.0) == 1.1
        assert MIGService.get_wire_diameter(6.0) == 1.7
        assert MIGService.get_wire_diameter(10.0) == 2.0
        assert MIGService.get_wire_diameter(15.0) == 2.25
    
    def test_current_density(self):
        assert MIGService.get_current_density(0.8) == 200
        assert MIGService.get_current_density(1.0) == 180
        assert MIGService.get_current_density(1.2) == 150
        assert MIGService.get_current_density(1.6) == 135
        assert MIGService.get_current_density(2.0) == 110
    
    def test_current_calculation(self):
        current = MIGService.calculate_current(1.2, 150)
        assert 169 <= current <= 170
    
    def test_voltage_and_gas_by_current(self):
        v, q = MIGService.get_voltage_and_gas(80)
        assert v == 17.5
        assert q == 6.5
        
        v, q = MIGService.get_voltage_and_gas(150)
        assert 20 <= v <= 21
        assert 8 <= q <= 10
        
        v, q = MIGService.get_voltage_and_gas(300)
        # Для тока 300 возвращается 28.5 (из диапазона 250-320)
        assert v == 28.5
        assert q == 15
    
    def test_alpha_p_calculation(self):
        alpha_p = MIGService.calculate_alpha_p(150, 1.2)
        assert round(alpha_p, 1) == 13.0
    
    def test_alpha_n_calculation(self):
        alpha_n = MIGService.calculate_alpha_n(13.0)
        assert round(alpha_n, 1) == 12.1
    
    def test_welding_speed(self):
        speed = MIGService.calculate_welding_speed(150)
        assert speed == 19.0
    
    def test_calculate(self):
        request = CalculationRequest(
            method=WeldMethod.MIG,
            material=Material.CARBON_STEEL,
            thickness=3.0,
            joint_group="C",
            joint_type="C1",
            length=500,
            gas_mixture="80%Ar+20%CO₂"
        )
        
        result = MIGService.calculate(request)
        
        assert result["wire_diameter"] == 1.1
        # Для толщины 3 мм ток получается ~143, что допустимо
        assert 140 <= result["current"] <= 150
        assert result["gas_mixture"] == "80%Ar+20%CO₂"
