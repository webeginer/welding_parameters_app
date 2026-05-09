from fastapi import APIRouter, Query, HTTPException
from backend.app.services.gost_14806_service import GOST14806Service
from backend.app.services.gost_5264_service import GOST5264Service
from backend.app.services.gost_14771_service import GOST14771Service
from backend.app.services.gost_23518_service import GOST23518Service

router = APIRouter(prefix="/api/gost", tags=["gost"])

GOST_SERVICES = {
    "gost_14806_80": GOST14806Service(),
    "gost_5264_80": GOST5264Service(),
    "gost_14771_76": GOST14771Service(),
    "gost_23518_79": GOST23518Service(),
}

@router.get("/list")
async def get_gost_list():
    return {
        "gosts": [
            {"id": "gost_14806_80", "name": "ГОСТ 14806-80", "description": "TIG сварка алюминия"},
            {"id": "gost_5264_80", "name": "ГОСТ 5264-80", "description": "Ручная дуговая сварка"},
            {"id": "gost_14771_76", "name": "ГОСТ 14771-76", "description": "MIG/MAG сварка"},
            {"id": "gost_23518_79", "name": "ГОСТ 23518-79", "description": "Сварка под острыми и тупыми углами"}
        ]
    }

@router.get("/joint-groups")
async def get_joint_groups(gost: str = Query(...)):
    if gost not in GOST_SERVICES:
        raise HTTPException(status_code=400, detail=f"Неизвестный ГОСТ: {gost}")
    service = GOST_SERVICES[gost]
    groups = service.get_joint_groups()
    return {"gost": gost, "groups": groups}

@router.get("/joint-types")
async def get_joint_types(gost: str = Query(...), group: str = Query(...)):
    if gost not in GOST_SERVICES:
        raise HTTPException(status_code=400, detail=f"Неизвестный ГОСТ: {gost}")
    service = GOST_SERVICES[gost]
    types = service.get_joint_types(group)
    return {"gost": gost, "group": group, "types": types}

@router.get("/processes")
async def get_weld_processes(gost: str = Query(...)):
    if gost not in GOST_SERVICES:
        raise HTTPException(status_code=400, detail=f"Неизвестный ГОСТ: {gost}")
    service = GOST_SERVICES[gost]
    if hasattr(service, "get_weld_processes"):
        processes = service.get_weld_processes()
        return {"gost": gost, "processes": processes}
    return {"gost": gost, "processes": []}
