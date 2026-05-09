class MIGService:
    
    @staticmethod
    def get_wire_diameter(thickness: float) -> float:
        if thickness <= 1:
            return 0.65
        elif thickness <= 2:
            return 0.9
        elif thickness <= 4:
            return 1.1
        elif thickness <= 8:
            return 1.7
        elif thickness <= 12:
            return 2.0
        else:
            return 2.25
    
    @staticmethod
    def get_current_density(diameter: float) -> float:
        if diameter <= 0.8:
            return 200
        elif diameter <= 1.0:
            return 180
        elif diameter <= 1.2:
            return 150
        elif diameter <= 1.6:
            return 135
        else:
            return 110
    
    @staticmethod
    def calculate_current(diameter: float, density: float = None) -> float:
        if density is None:
            density = MIGService.get_current_density(diameter)
        import math
        area = math.pi * (diameter ** 2) / 4
        return area * density
    
    @staticmethod
    def get_voltage_and_gas(current: float) -> tuple:
        if current <= 90:
            return 17.5, 6.5
        elif current <= 120:
            return 19, 8
        elif current <= 180:
            return 20.5, 9
        elif current <= 220:
            return 23.5, 11
        elif current <= 280:
            return 26.5, 13.5
        elif current <= 320:
            return 28.5, 15
        else:
            return 30, 17
    
    @staticmethod
    def calculate_alpha_p(current: float, diameter: float) -> float:
        return 3.0 + 0.08 * (current / diameter)
    
    @staticmethod
    def get_loss_coefficient() -> float:
        return 0.07
    
    @staticmethod
    def calculate_alpha_n(alpha_p: float, psi: float = None) -> float:
        if psi is None:
            psi = MIGService.get_loss_coefficient()
        return alpha_p * (1 - psi)
    
    @staticmethod
    def calculate_welding_speed(current: float) -> float:
        return round(15 + (current - 100) * 0.08, 1)
    
    @staticmethod
    def calculate(request) -> dict:
        thickness = request.thickness
        gas_mixture = request.gas_mixture or "100% Ar"
        
        diameter = MIGService.get_wire_diameter(thickness)
        density = MIGService.get_current_density(diameter)
        current = MIGService.calculate_current(diameter, density)
        voltage, gas_flow = MIGService.get_voltage_and_gas(current)
        
        alpha_p = MIGService.calculate_alpha_p(current, diameter)
        alpha_n = MIGService.calculate_alpha_n(alpha_p)
        welding_speed = MIGService.calculate_welding_speed(current)
        
        return {
            "wire_diameter": round(diameter, 2),
            "current": round(current),
            "voltage": voltage,
            "welding_speed": welding_speed,
            "gas_flow_rate": gas_flow,
            "gas_mixture": gas_mixture,
            "polarity": "Постоянный ток, обратная полярность",
            "deposition_coefficient": round(alpha_n, 1)
        }
