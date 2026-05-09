import pytest
from backend.app.services.calculation_service import CalculationService
from backend.app.models import CalculationRequest, WeldMethod, Material


class TestCalculationService:
    
    def test_calculate_tig_aluminum(self):
        request = CalculationRequest(
            method=WeldMethod.TIG,
            material=Material.ALUMINUM,
            thickness=4.0,
            joint_group="C",
            joint_type="C4",
            length=500
        )
        result = CalculationService.calculate(request)
        assert result["success"] is True
        assert result["method"] == "TIG"
    
    def test_calculate_tig_carbon_steel(self):
        request = CalculationRequest(
            method=WeldMethod.TIG,
            material=Material.CARBON_STEEL,
            thickness=3.0,
            joint_group="C",
            joint_type="C1",
            length=500
        )
        result = CalculationService.calculate(request)
        params = result["parameters"]
        assert params["polarity"] == "Постоянный ток, прямая полярность"
    
    def test_calculate_mma(self):
        request = CalculationRequest(
            method=WeldMethod.MMA,
            material=Material.CARBON_STEEL,
            thickness=6.0,
            joint_group="C",
            joint_type="C1",
            length=500,
            position="lower"
        )
        result = CalculationService.calculate(request)
        assert result["success"] is True
        assert result["method"] == "MMA"
    
    def test_calculate_mma_vertical(self):
        request = CalculationRequest(
            method=WeldMethod.MMA,
            material=Material.CARBON_STEEL,
            thickness=6.0,
            joint_group="C",
            joint_type="C1",
            length=500,
            position="vertical"
        )
        result = CalculationService.calculate(request)
        params = result["parameters"]
        assert params["current"] <= 145
    
    def test_calculate_mig(self):
        request = CalculationRequest(
            method=WeldMethod.MIG,
            material=Material.CARBON_STEEL,
            thickness=4.0,
            joint_group="C",
            joint_type="C1",
            length=500,
            gas_mixture="80%Ar+20%CO₂"
        )
        result = CalculationService.calculate(request)
        assert result["success"] is True
        assert result["method"] == "MIG-MAG"
        params = result["parameters"]
        assert "wire_diameter" in params
        assert "current" in params
        assert "voltage" in params
        assert params["gas_mixture"] == "80%Ar+20%CO₂"
    
    def test_invalid_method(self):
        with pytest.raises(ValueError):
            request = CalculationRequest(
                method=WeldMethod.TIG,
                material=Material.CARBON_STEEL,
                thickness=4.0,
                joint_group="C",
                joint_type="C1",
                length=500
            )
            request.method = "INVALID"
            CalculationService.calculate(request)
