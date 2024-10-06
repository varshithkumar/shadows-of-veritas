# backend/app/routers/cases.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(
    prefix="/cases",
    tags=["cases"],
)

@router.get("/", response_model=List[schemas.Case])
async def read_cases(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    cases = await crud.get_cases(db, skip=skip, limit=limit)
    # Convert ORM instances to Pydantic models
    return [schemas.Case.from_orm(case) for case in cases]

@router.get("/{case_id}", response_model=schemas.Case)
async def read_case(case_id: int, db: AsyncSession = Depends(get_db)):
    db_case = await crud.get_case(db, case_id=case_id)
    if db_case is None:
        raise HTTPException(status_code=404, detail="Case not found")
    return schemas.Case.from_orm(db_case)
