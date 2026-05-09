"""
Тесты для TIG калькулятора с учётом ГОСТ 14806-80
"""
import pytest
from backend.app.services.tig_service import TIGCalculator
from backend.app.models import Material, JointGroup


class TestTIGCalculator:
    """Тесты для TIG сварки"""
    
    def test_gost_selection_aluminum(self):
        """Тест выбора ГОСТ для алюминия"""
        gost = TIGCalculator.select_gost(Material.ALUMINUM)
        assert gost == "ГОСТ 14806-80"
    
    def test_gost_selection_carbon_steel(self):
        """Тест выбора ГОСТ для углеродистой стали"""
        gost = TIGCalculator.select_gost(Material.CARBON_STEEL)
        assert gost == "ГОСТ 14771-76"
    
    def test_current_selection_by_diameter_dc(self):
        """Тест выбора тока для DC прямой полярности (табл.6 методички)"""
        I = TIGCalculator.get_current_dc(diameter=4.0)
        # Для d=4 мм, DC прямая: 250-340 А
        assert 250 <= I <= 340
    
    def test_current_selection_by_diameter_ac(self):
        """Тест выбора тока для AC (табл.6 методички)"""
        I = TIGCalculator.get_current_ac(diameter=4.0)
        # Для d=4 мм, AC: 140-220 А
        assert 140 <= I <= 220
    
    def test_tungsten_diameter_for_aluminum(self):
        """Тест выбора диаметра вольфрама для алюминия (табл.5 методички)"""
        d = TIGCalculator.get_tungsten_diameter(
            material=Material.ALUMINUM,
            thickness=4.0
        )
        # Для алюминия S=4 мм → d=4 мм
        assert d == 4.0
    
    def test_gas_flow_rate_for_aluminum(self):
        """Тест расхода газа для алюминия (табл.8 методички)"""
        Q = TIGCalculator.get_gas_flow(
            material=Material.ALUMINUM,
            thickness=4.0,
            current=180
        )
        # S=4 мм, I=160-210 → расход 7-8 л/мин
        assert 7 <= Q <= 8
    
    def test_voltage_range(self):
        """Тест диапазона напряжения"""
        U = TIGCalculator.get_voltage()
        assert 11 <= U <= 14
