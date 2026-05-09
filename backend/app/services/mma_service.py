class MMAService:
    """Сервис для расчёта параметров ручной дуговой сварки (MMA)"""
    
    # Таблица 1: диаметр электрода от толщины металла
    @staticmethod
    def get_electrode_diameter(thickness: float) -> float:
        if thickness <= 2:
            return 1.6
        elif thickness <= 3:
            return 2.5
        elif thickness <= 5:
            return 3.0
        elif thickness <= 10:
            return 4.0
        elif thickness <= 15:
            return 5.0
        else:
            return 6.0
    
    # Таблица 2: коэффициент k от диаметра электрода
    @staticmethod
    def get_k_coefficient(diameter: float) -> float:
        if diameter <= 2:
            return 27.5  # среднее 25-30
        elif diameter <= 4:
            return 37.5  # среднее 30-45
        else:
            return 52.5  # среднее 45-60
    
    # Расчёт тока: I = k * dэ
    @staticmethod
    def calculate_current(diameter: float) -> float:
        k = MMAService.get_k_coefficient(diameter)
        return k * diameter
    
    # Коррекция тока для положения шва
    @staticmethod
    def correct_current(current: float, position: str) -> float:
        if position == "vertical":
            return current * 0.9  # -10%
        elif position == "ceiling":
            return current * 0.85  # -15%
        else:  # lower
            return current
    
    # Напряжение на дуге
    @staticmethod
    def get_voltage(electrode_brand: str = None) -> float:
        # Для большинства электродов 22-28 В
        return 25.0
    
    # Скорость сварки (упрощённо)
    @staticmethod
    def calculate_welding_speed(current: float) -> float:
        # Ориентировочно 5-15 м/ч
        return round(8.0 + (current - 100) * 0.03, 1)
    
    @staticmethod
    def calculate(request) -> dict:
        thickness = request.thickness
        position = request.position
        
        diameter = MMAService.get_electrode_diameter(thickness)
        current_raw = MMAService.calculate_current(diameter)
        current = MMAService.correct_current(current_raw, position)
        voltage = MMAService.get_voltage(request.electrode_brand)
        welding_speed = MMAService.calculate_welding_speed(current)
        
        return {
            "electrode_diameter": diameter,
            "current": round(current),
            "voltage": voltage,
            "welding_speed": welding_speed,
            "polarity": "Постоянный или переменный ток",
            "electrode_brand": request.electrode_brand or "Не указана"
        }
