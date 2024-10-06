from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_db
from .. import crud, schemas
from ..services import llm_service

router = APIRouter(
    prefix="/llm",
    tags=["llm"],
)

@router.post("/generate_case/", response_model=schemas.Case)
async def generate_case(db: AsyncSession = Depends(get_db)):
    try:
        case_data = await llm_service.generate_case()
        case_create = schemas.CaseCreate(**case_data)
        db_case = await crud.create_case(db, case_create)
        return schemas.Case.from_orm(db_case)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
