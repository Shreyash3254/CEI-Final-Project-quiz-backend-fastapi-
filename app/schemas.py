"""
Pydantic schemas for request validation and response serialization.

Defines schemas for creating, updating, and returning Questions and Choices.
"""

from pydantic import BaseModel, ConfigDict
from typing import Optional, List


# ---------------------------------------------------------------------------
# Choice Schemas
# ---------------------------------------------------------------------------

class ChoiceCreate(BaseModel):
    """Schema for creating a new choice."""
    choice_text: str
    is_correct: bool
    question_id: int


class ChoiceUpdate(BaseModel):
    """Schema for updating an existing choice."""
    choice_text: str
    is_correct: bool
    question_id: int


class ChoiceResponse(BaseModel):
    """Schema for returning a choice in API responses."""
    id: int
    choice_text: str
    is_correct: bool
    question_id: int

    # Enable ORM mode for SQLAlchemy model serialization
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Question Schemas
# ---------------------------------------------------------------------------

class QuestionCreate(BaseModel):
    """Schema for creating a new question."""
    question_text: str
    category: Optional[str] = None


class QuestionUpdate(BaseModel):
    """Schema for updating an existing question."""
    question_text: str
    category: Optional[str] = None


class QuestionResponse(BaseModel):
    """Schema for returning a question in API responses."""
    id: int
    question_text: str
    category: Optional[str] = None
    choices: List[ChoiceResponse] = []

    # Enable ORM mode for SQLAlchemy model serialization
    model_config = ConfigDict(from_attributes=True)
