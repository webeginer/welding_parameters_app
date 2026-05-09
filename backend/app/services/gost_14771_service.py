"""ГОСТ 14771-76 — Дуговая сварка в защитном газе. Соединения сварные."""

class GOST14771Service:
    """Сервис для работы с ГОСТ 14771-76 (MIG/MAG)"""
    
    # Группы соединений (табл.1)
    JOINT_GROUPS = {
        "C": "Стыковые",
        "У": "Угловые", 
        "Т": "Тавровые",
        "Н": "Нахлесточные"
    }
    
    # Типы соединений по группам
    JOINTS_BY_GROUP = {
        "C": ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", 
              "C11", "C12", "C13", "C14", "C15", "C16", "C17", "C18", "C19", 
              "C20", "C21", "C22", "C23", "C24", "C25", "C26", "C27", "C28"],
        "У": ["У1", "У2", "У3", "У4", "У5", "У6", "У7", "У8", "У9", "У10"],
        "Т": ["Т1", "Т2", "Т3", "Т4", "Т5", "Т6", "Т7", "Т8", "Т9"],
        "Н": ["Н1", "Н2"]
    }
    
    # Способы сварки
    WELD_PROCESSES = {
        "ИН": "В инертных газах, неплавящимся электродом без присадки",
        "ИНп": "В инертных газах, неплавящимся электродом с присадкой",
        "ИП": "В инертных газах, плавящимся электродом",
        "УП": "В углекислом газе, плавящимся электродом"
    }
    
    @staticmethod
    def get_joint_groups() -> list:
        """Возвращает список групп соединений"""
        return [{"code": k, "name": v} for k, v in GOST14771Service.JOINT_GROUPS.items()]
    
    @staticmethod
    def get_joint_types(group: str) -> list:
        """Возвращает список типов соединений для группы"""
        types = GOST14771Service.JOINTS_BY_GROUP.get(group, [])
        return [{"code": t} for t in types]
    
    @staticmethod
    def get_weld_processes() -> list:
        """Возвращает список способов сварки"""
        return [{"code": k, "name": v} for k, v in GOST14771Service.WELD_PROCESSES.items()]
    
    @staticmethod
    def get_constructive_elements(joint_type: str, thickness: float, process: str = "ИП") -> dict:
        """Возвращает конструктивные элементы для типа соединения"""
        elements = {
            "b": 0,      # зазор
            "c": 0,      # притупление
            "e": None,   # ширина шва
            "g": None,   # усиление
            "R": None,   # радиус скругления
            "α": 0,      # угол скоса
        }
        
        # C1 — стыковое без скоса (табл.2)
        if joint_type == "C1":
            if thickness <= 4:
                elements["b"] = 0
                elements["e"] = 1.5 * thickness + 2.5
                if thickness <= 0.9:
                    elements["b"] = 0
                elif thickness <= 1.4:
                    elements["b"] = 0.3
                else:
                    elements["b"] = 0.5
        
        # C2 — с отбортовкой (табл.5)
        elif joint_type == "C2":
            if thickness <= 1.5:
                elements["b"] = 0.5
                elements["e"] = 7.0
                elements["g"] = 1.0
            elif thickness <= 2.5:
                elements["b"] = 0.8
                elements["e"] = 8.0
                elements["g"] = 1.5
        
        return elements
    
    @staticmethod
    def get_thickness_range(joint_type: str, process: str = "ИП") -> tuple:
        """Возвращает допустимый диапазон толщин для типа соединения"""
        ranges = {
            "C1": (0.5, 4.0),
            "C2": (0.5, 4.0),
            "C3": (0.5, 4.0),
            "C4": (0.8, 4.0),
            "C5": (0.8, 4.0),
            "C6": (0.8, 4.0),
        }
        
        # Для УП (углекислый газ) диапазоны шире
        if process == "УП":
            ranges["C1"] = (0.5, 60.0)
            ranges["C2"] = (0.5, 60.0)
        
        return ranges.get(joint_type, (0.5, 60.0))
    
    @staticmethod
    def calculate_Fn(joint_type: str, thickness: float, elements: dict) -> float:
        """Расчёт площади поперечного сечения шва"""
        if joint_type.startswith("C"):
            b = elements.get("b", 0)
            e = elements.get("e", thickness * 2)
            g = elements.get("g", thickness * 0.2)
            return (thickness * b + 0.5 * e * g) / 100
        elif joint_type.startswith("У"):
            k = thickness
            return (0.5 * k * k + 1.05 * k) / 100
        else:
            return (thickness * thickness) / 100
