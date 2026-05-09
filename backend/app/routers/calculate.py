from fastapi import APIRouter, HTTPException
from backend.app.models import CalculationRequest
from backend.app.services.calculation_service import CalculationService

router = APIRouter(prefix="/api", tags=["calculate"])

@router.post("/calculate")
async def calculate(request: CalculationRequest):
    try:
        result = CalculationService.calculate(request)
        # result уже содержит success, method, parameters
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
