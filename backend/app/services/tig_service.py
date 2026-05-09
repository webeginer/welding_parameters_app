from backend.app.models import Material

class TIGCalculator:
    @staticmethod
    def select_gost(material: Material):
        if material == Material.ALUMINUM:
            return "ГОСТ 14806-80"
        else:
            return "ГОСТ 14771-76"
    
    @staticmethod
    def get_current_dc(diameter: float):
        currents = {1.5: (65, 160), 2: (65, 160), 3: (140, 180), 4: (250, 340), 5: (300, 400), 6: (350, 450)}
        return currents.get(diameter, (100, 200))[0]
    
    @staticmethod
    def get_current_ac(diameter: float):
        currents = {1.5: (20, 100), 2: (20, 100), 3: (100, 160), 4: (140, 220), 5: (200, 280), 6: (250, 300)}
        return currents.get(diameter, (100, 200))[0]
    
    @staticmethod
    def get_tungsten_diameter(material: Material, thickness: float):
        if material == Material.ALUMINUM:
            if thickness <= 1: return 1.5
            elif thickness <= 2: return 2
            elif thickness <= 4: return 4
            elif thickness <= 6: return 4
            else: return 5
        else:
            if thickness <= 0.5: return 1
            elif thickness <= 1: return 1.5
            elif thickness <= 2: return 2
            elif thickness <= 3: return 3
            elif thickness <= 4: return 4
            else: return 6
    
    @staticmethod
    def get_gas_flow(material: Material, thickness: float, current: float):
        if material == Material.ALUMINUM:
            if thickness <= 2: return 5.5
            elif thickness <= 4: return 7.5
            else: return 11
        else:
            if thickness <= 2: return 9
            else: return 11
    
    @staticmethod
    def get_voltage():
        return 12.5
