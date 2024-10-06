# backend/app/models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Case(Base):
    __tablename__ = 'cases'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)

    characters = relationship("Character", back_populates="case")
    clues = relationship("Clue", back_populates="case")

class Character(Base):
    __tablename__ = 'characters'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    background = Column(Text)
    case_id = Column(Integer, ForeignKey('cases.id'))

    case = relationship("Case", back_populates="characters")
    dialogues = relationship("Dialogue", back_populates="character")

class Dialogue(Base):
    __tablename__ = 'dialogues'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    character_id = Column(Integer, ForeignKey('characters.id'))

    character = relationship("Character", back_populates="dialogues")
    options = relationship("DialogueOption", back_populates="dialogue")

class DialogueOption(Base):
    __tablename__ = 'dialogue_options'

    id = Column(Integer, primary_key=True, index=True)
    response = Column(Text)
    next_dialogue_id = Column(Integer)
    dialogue_id = Column(Integer, ForeignKey('dialogues.id'))

    dialogue = relationship("Dialogue", back_populates="options")

class Clue(Base):
    __tablename__ = 'clues'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    location = Column(String)
    case_id = Column(Integer, ForeignKey('cases.id'))

    case = relationship("Case", back_populates="clues")
