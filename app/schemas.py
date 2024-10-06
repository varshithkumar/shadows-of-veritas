# backend/app/schemas.py
from typing import List, Optional
from pydantic import BaseModel

class DialogueOptionBase(BaseModel):
    response: str
    next_dialogue_id: Optional[int] = None

class DialogueOptionCreate(DialogueOptionBase):
    pass

class DialogueOption(DialogueOptionBase):
    id: int

    class Config:
        from_attributes = True

class DialogueBase(BaseModel):
    text: str

class DialogueCreate(DialogueBase):
    options: List[DialogueOptionCreate] = []

class Dialogue(DialogueBase):
    id: int
    options: List[DialogueOption] = []

    class Config:
        from_attributes = True

class CharacterBase(BaseModel):
    name: str
    background: str

class CharacterCreate(CharacterBase):
    dialogues: List[DialogueCreate] = []

class Character(CharacterBase):
    id: int
    dialogues: List[Dialogue] = []

    class Config:
        from_attributes = True

class ClueBase(BaseModel):
    description: str
    location: str

class ClueCreate(ClueBase):
    pass

class Clue(ClueBase):
    id: int

    class Config:
        from_attributes = True

class CaseBase(BaseModel):
    title: str
    description: str

class CaseCreate(CaseBase):
    characters: List[CharacterCreate] = []
    clues: List[ClueCreate] = []

class Case(CaseBase):
    id: int
    characters: List[Character] = []
    clues: List[Clue] = []

    class Config:
        from_attributes = True
