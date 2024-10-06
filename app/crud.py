# backend/app/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from . import models, schemas

async def create_case(db: AsyncSession, case_data: schemas.CaseCreate):
    db_case = models.Case(title=case_data.title, description=case_data.description)
    db.add(db_case)
    await db.flush()

    # Add characters
    for character_data in case_data.characters:
        db_character = models.Character(
            name=character_data.name,
            background=character_data.background,
            case_id=db_case.id,
        )
        db.add(db_character)
        await db.flush()

        # Add dialogues
        for dialogue_data in character_data.dialogues:
            db_dialogue = models.Dialogue(
                text=dialogue_data.text,
                character_id=db_character.id,
            )
            db.add(db_dialogue)
            await db.flush()

            # Add dialogue options
            for option_data in dialogue_data.options:
                db_option = models.DialogueOption(
                    response=option_data.response,
                    next_dialogue_id=option_data.next_dialogue_id,
                    dialogue_id=db_dialogue.id,
                )
                db.add(db_option)

    # Add clues
    for clue_data in case_data.clues:
        db_clue = models.Clue(
            description=clue_data.description,
            location=clue_data.location,
            case_id=db_case.id,
        )
        db.add(db_clue)

    await db.commit()
    # Instead of refreshing, we fetch the case with all relationships eagerly loaded
    result = await db.execute(
        select(models.Case)
        .options(
            selectinload(models.Case.characters)
            .selectinload(models.Character.dialogues)
            .selectinload(models.Dialogue.options),
            selectinload(models.Case.clues),
        )
        .where(models.Case.id == db_case.id)
    )
    db_case_with_relations = result.scalars().first()
    return db_case_with_relations


# Function to get a case by ID
async def get_case(db: AsyncSession, case_id: int):
    result = await db.execute(
        select(models.Case)
        .options(
            selectinload(models.Case.characters)
            .selectinload(models.Character.dialogues)
            .selectinload(models.Dialogue.options),
            selectinload(models.Case.clues),
        )
        .where(models.Case.id == case_id)
    )
    return result.scalars().first()

# Function to get all cases
async def get_cases(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Case)
        .options(
            selectinload(models.Case.characters)
            .selectinload(models.Character.dialogues)
            .selectinload(models.Dialogue.options),
            selectinload(models.Case.clues),
        )
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_character(db: AsyncSession, character_id: int):
    result = await db.execute(
        select(models.Character)
        .options(
            selectinload(models.Character.dialogues)
            .selectinload(models.Dialogue.options)
        )
        .where(models.Character.id == character_id)
    )
    return result.scalars().first()
