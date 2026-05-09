"""ГОСТ 23518-79 — Дуговая сварка в защитных газах. Соединения под острыми и тупыми углами."""

class GOST23518Service:
    """Сервис для работы с ГОСТ 23518-79 (сварка под углом)"""
    
    # Группы соединений (табл.1)
    JOINT_GROUPS = {
        "У": "Угловые",
        "Т": "Тавровые"
    }
    
    # Типы соединений по группам
    JOINTS_BY_GROUP = {
        "У": ["У1", "У2", "У3", "У4", "У5", "У6", "У7", "У8", "У9", "У10"],
        "Т": ["Т1", "Т2", "Т3", "Т4", "Т5", "Т6", "Т7", "Т8", "Т9"]
    }
    
    # Способы сварки
    WELD_PROCESSES = {
        "ИН": "В инертных газах, неплавящимся электродом без присадки",
        "ИНп": "В инертных газах, неплавящимся электродом с присадкой",
        "ИП": "В инертных газах и их смесях, плавящимся электродом",
        "УП": "В углекислом газе, плавящимся электродом"
    }
    
    @staticmethod
    def get_joint_groups() -> list:
        """Возвращает список групп соединений"""
        return [{"code": k, "name": v} for k, v in GOST23518Service.JOINT_GROUPS.items()]
    
    @staticmethod
    def get_joint_types(group: str) -> list:
        """Возвращает список типов соединений для группы"""
        types = GOST23518Service.JOINTS_BY_GROUP.get(group, [])
        return [{"code": t} for t in types]
    
    @staticmethod
    def get_weld_processes() -> list:
        """Возвращает список способов сварки"""
        return [{"code": k, "name": v} for k, v in GOST23518Service.WELD_PROCESSES.items()]
    
    @staticmethod
    def get_constructive_elements(joint_type: str, thickness: float, angle: int = 90) -> dict:
        """Возвращает конструктивные элементы для типа соединения"""
        elements = {
            "b": 0,      # зазор
            "e": None,   # ширина шва
            "g": None,   # усиление
            "β": angle,  # угол соединения
        }
        
        # У1 — угловое без скоса (табл.2)
        if joint_type == "У1":
            if thickness <= 2:
                elements["b"] = 0
                elements["e"] = 2 * thickness + 3
        
        # У2 — угловое одностороннее (табл.3)
        elif joint_type == "У2":
            if thickness <= 3:
                elements["b"] = thickness
                elements["e"] = thickness + 5
        
        # Т1 — тавровое без скоса (табл.12)
        elif joint_type == "Т1":
            if thickness <= 10:
                elements["e"] = 4 + thickness * 0.5
        
        return elements
    
    @staticmethod
    def get_thickness_range(joint_type: str, process: str = "ИП") -> tuple:
        """Возвращает допустимый диапазон толщин для типа соединения"""
        ranges = {
            "У1": (0.5, 4.0),
            "У2": (0.5, 4.0),
            "У3": (0.5, 4.0),
            "Т1": (0.8, 40.0),
        }
        return ranges.get(joint_type, (0.5, 40.0))
    
    @staticmethod
    def get_angle_range(joint_type: str) -> tuple:
        """Возвращает допустимый диапазон углов соединения"""
        angle_ranges = {
            "У1": (0, 179),
            "У2": (0, 179),
            "Т1": (91, 175),
        }
        return angle_ranges.get(joint_type, (0, 180))
