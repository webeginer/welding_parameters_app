class GOST14806Service:
    def __init__(self, db=None):
        self.db = db
    
    def get_joint_groups(self):
        return [{"code": "C", "name": "Стыковые"}, {"code": "У", "name": "Угловые"}, {"code": "Т", "name": "Тавровые"}, {"code": "Н", "name": "Нахлесточные"}]
    
    def get_joint_types_by_group(self, group):
        if group == "C":
            return [{"code": "C1"}, {"code": "C4"}, {"code": "C44"}]
        elif group == "У":
            return [{"code": "У1"}, {"code": "У4"}, {"code": "У14"}]
        else:
            return []
    
    def get_constructive_elements(self, joint_type, thickness, process):
        if joint_type == "C7":
            return {"b": 16, "e": 19, "g": 2.0, "R": 2}
        elif joint_type == "T1":
            return {"b": 16, "e": 19, "g": 2.0, "K": 3}
        else:
            return {"b": 16, "e": 19, "g": 2.0}
    
    def validate_thickness(self, joint_type, thickness, process):
        if joint_type == "C4":
            return 6.0 <= thickness <= 8.0
        return 0.8 <= thickness <= 60.0
    
    def get_available_processes(self, joint_type):
        return ["РИНп", "АИНп", "АИНп-3", "АИП", "ПИП"]
    
    def calculate_Fn(self, joint_type, thickness, elements):
        return (thickness * elements.get("b", 0) + 0.75 * elements.get("e", 0) * elements.get("g", 0)) / 100
    
    def get_applicable_tables(self, joint_type):
        return ["табл.4", "табл.5", "табл.6"]
