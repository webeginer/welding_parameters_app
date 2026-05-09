from backend.app.models import CalculationRequest, Material, WeldMethod
from backend.app.services.tig_service import TIGCalculator
from backend.app.services.mma_service import MMAService
from backend.app.services.mig_service import MIGService


class CalculationService:
    @staticmethod
    def calculate_tig(request: CalculationRequest) -> dict:
        """Расчёт параметров для TIG сварки"""
        material = request.material
        thickness = request.thickness
        
        tungsten_diameter = TIGCalculator.get_tungsten_diameter(material, thickness)
        
        if material == Material.ALUMINUM:
            current = TIGCalculator.get_current_ac(tungsten_diameter)
            polarity = "Переменный ток"
        else:
            current = TIGCalculator.get_current_dc(tungsten_diameter)
            polarity = "Постоянный ток, прямая полярность"
        
        voltage = TIGCalculator.get_voltage()
        gas_flow = TIGCalculator.get_gas_flow(material, thickness, current)
        welding_speed = 0.3
        
        return {
            "success": True,
            "method": request.method.value,
            "parameters": {
                "electrode_diameter": tungsten_diameter,
                "current": current,
                "voltage": voltage,
                "welding_speed": welding_speed,
                "polarity": polarity,
                "gas_flow_rate": gas_flow
            }
        }
    
    @staticmethod
    def calculate_mma(request: CalculationRequest) -> dict:
        """Расчёт параметров для MMA сварки"""
        params = MMAService.calculate(request)
        return {
            "success": True,
            "method": request.method.value,
            "parameters": params
        }
    
    @staticmethod
    def calculate_mig(request: CalculationRequest) -> dict:
        """Расчёт параметров для MIG/MAG сварки"""
        params = MIGService.calculate(request)
        return {
            "success": True,
            "method": request.method.value,
            "parameters": params
        }
    
    @staticmethod
    def calculate(request: CalculationRequest) -> dict:
        if request.method == WeldMethod.TIG:
            return CalculationService.calculate_tig(request)
        elif request.method == WeldMethod.MMA:
            return CalculationService.calculate_mma(request)
        elif request.method == WeldMethod.MIG:
            return CalculationService.calculate_mig(request)
        else:
            raise ValueError(f"Unknown method: {request.method}")
