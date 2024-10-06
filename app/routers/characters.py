# backend/app/routers/characters.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(
    prefix="/characters",
    tags=["characters"],
)

@router.get("/{character_id}", response_model=schemas.Character)
async def read_character(character_id: int, db: AsyncSession = Depends(get_db)):
    db_character = await crud.get_character(db, character_id=character_id)
    if db_character is None:
        raise HTTPException(status_code=404, detail="Character not found")
    return schemas.Character.from_orm(db_character)
