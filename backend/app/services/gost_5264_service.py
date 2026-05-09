"""ГОСТ 5264-80 — Ручная дуговая сварка. Соединения сварные."""

class GOST5264Service:
    """Сервис для работы с ГОСТ 5264-80"""
    
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
              "C20", "C21", "C22", "C23", "C24", "C25", "C26", "C27", "C28", 
              "C29", "C30", "C31", "C32", "C33", "C34", "C35", "C36", "C37", 
              "C38", "C39", "C40", "C41", "C42", "C43", "C44", "C45"],
        "У": ["У1", "У2", "У3", "У4", "У5", "У6", "У7", "У8", "У9", "У10"],
        "Т": ["Т1", "Т2", "Т3", "Т4", "Т5", "Т6", "Т7", "Т8", "Т9"],
        "Н": ["Н1", "Н2"]
    }
    
    @staticmethod
    def get_joint_groups() -> list:
        """Возвращает список групп соединений"""
        return [{"code": k, "name": v} for k, v in GOST5264Service.JOINT_GROUPS.items()]
    
    @staticmethod
    def get_joint_types(group: str) -> list:
        """Возвращает список типов соединений для группы"""
        types = GOST5264Service.JOINTS_BY_GROUP.get(group, [])
        return [{"code": t} for t in types]
    
    @staticmethod
    def get_constructive_elements(joint_type: str, thickness: float) -> dict:
        """Возвращает конструктивные элементы для типа соединения"""
        elements = {
            "b": 0,      # зазор
            "c": 0,      # притупление
            "e": None,   # ширина шва
            "g": None,   # усиление
            "R": None,   # радиус скругления
        }
        
        # C1 — стыковое без скоса кромок (табл.2)
        if joint_type == "C1":
            if 1 <= thickness <= 4:
                elements["b"] = 0
                elements["e"] = 2 * thickness + 3
        
        # C2 — стыковое на съемной подкладке (табл.5)
        elif joint_type == "C2":
            if 1.0 <= thickness <= 1.5:
                elements["b"] = 0
                elements["e"] = 6
                elements["g"] = 1.0
            elif 1.5 < thickness <= 3.0:
                elements["b"] = 1
                elements["e"] = 7
                elements["g"] = 1.5
            elif 3.0 < thickness <= 4.0:
                elements["b"] = 2
                elements["e"] = 8
                elements["g"] = 2.0
        
        return elements
    
    @staticmethod
    def get_thickness_range(joint_type: str) -> tuple:
        """Возвращает допустимый диапазон толщин для типа соединения"""
        ranges = {
            "C1": (1, 4),
            "C2": (1, 4),
            "C3": (1, 4),
            "C4": (1, 4),
            "C5": (1, 4),
            "C6": (1, 4),
            "C7": (2, 5),
            "C8": (3, 60),
            "C9": (3, 60),
        }
        return ranges.get(joint_type, (1, 60))
    
    @staticmethod
    def calculate_Fn(joint_type: str, thickness: float, elements: dict) -> float:
        """Расчёт площади поперечного сечения шва"""
        if joint_type.startswith("C"):
            # Стыковые соединения
            b = elements.get("b", 0)
            e = elements.get("e", thickness * 2)
            g = elements.get("g", thickness * 0.2)
            return (thickness * b + 0.5 * e * g) / 100  # см²
        elif joint_type.startswith("У"):
            # Угловые соединения
            k = thickness  # катет условно
            return (0.5 * k * k + 1.05 * k) / 100
        else:
            return (thickness * thickness) / 100
