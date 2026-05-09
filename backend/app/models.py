from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional

class Material(str, Enum):
    ALUMINUM = "Алюминий"
    CARBON_STEEL = "Сталь углеродистая"
    STAINLESS_STEEL = "Нержавеющая"

class WeldMethod(str, Enum):
    MMA = "MMA"
    TIG = "TIG"
    MIG = "MIG-MAG"

class JointGroup(str, Enum):
    C = "C"
    U = "У"
    T = "Т"
    H = "Н"

class JointType(str, Enum):
    C1 = "C1"
    C4 = "C4"
    C44 = "C44"
    U1 = "У1"
    U4 = "У4"
    U14 = "У14"

class WeldProcess(str, Enum):
    RINP = "РИНп"
    AINP = "АИНп"
    AINP3 = "АИНп-3"
    AIP = "АИП"
    PIP = "ПИП"

class CalculationRequest(BaseModel):
    method: WeldMethod
    material: Material
    thickness: float = Field(..., ge=0.5, le=100)
    joint_group: str
    joint_type: str
    length: float = Field(..., ge=0)
    position: str = "lower"
    with_filler: bool = True
    electrode_brand: Optional[str] = None
    gas_mixture: Optional[str] = None
    gost_standard: Optional[str] = None
