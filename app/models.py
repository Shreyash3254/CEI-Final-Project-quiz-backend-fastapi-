"""
SQLAlchemy ORM models for the Quiz application.

Defines the Question and Choice tables and their relationship.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Question(Base):
    """
    Represents a quiz question.

    Fields:
        id            — Primary key
        question_text — The text of the question (required)
        category      — Optional category for the question
    """
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, nullable=False)
    category = Column(String, nullable=True)

    # One Question → Many Choices relationship
    # cascade="all, delete-orphan" ensures choices are deleted when the question is deleted
    choices = relationship("Choice", back_populates="question", cascade="all, delete-orphan")


class Choice(Base):
    """
    Represents an answer choice for a quiz question.

    Fields:
        id          — Primary key
        choice_text — The text of the choice (required)
        is_correct  — Whether this choice is the correct answer (required)
        question_id — Foreign key linking to the parent question
    """
    __tablename__ = "choices"

    id = Column(Integer, primary_key=True, index=True)
    choice_text = Column(String, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)

    # Back-reference to the parent question
    question = relationship("Question", back_populates="choices")
