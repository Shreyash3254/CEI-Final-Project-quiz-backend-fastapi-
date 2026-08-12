"""
CRUD (Create, Read, Update, Delete) operations for Questions and Choices.

All database operations are performed through SQLAlchemy ORM sessions.
"""

from sqlalchemy.orm import Session

from app import models, schemas


# ---------------------------------------------------------------------------
# Question CRUD Operations
# ---------------------------------------------------------------------------

def create_question(db: Session, question: schemas.QuestionCreate) -> models.Question:
    """Create a new question in the database."""
    db_question = models.Question(
        question_text=question.question_text,
        category=question.category
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_all_questions(db: Session) -> list[models.Question]:
    """Retrieve all questions from the database."""
    return db.query(models.Question).all()


def get_question_by_id(db: Session, question_id: int) -> models.Question | None:
    """Retrieve a single question by its ID. Returns None if not found."""
    return db.query(models.Question).filter(models.Question.id == question_id).first()


def update_question(
    db: Session, question_id: int, question_data: schemas.QuestionUpdate
) -> models.Question | None:
    """Update an existing question. Returns None if the question does not exist."""
    db_question = get_question_by_id(db, question_id)
    if db_question is None:
        return None

    db_question.question_text = question_data.question_text
    db_question.category = question_data.category
    db.commit()
    db.refresh(db_question)
    return db_question


def delete_question(db: Session, question_id: int) -> models.Question | None:
    """
    Delete a question and its associated choices (via cascade).
    Returns None if the question does not exist.
    """
    db_question = get_question_by_id(db, question_id)
    if db_question is None:
        return None

    db.delete(db_question)
    db.commit()
    return db_question


# ---------------------------------------------------------------------------
# Choice CRUD Operations
# ---------------------------------------------------------------------------

def create_choice(db: Session, choice: schemas.ChoiceCreate) -> models.Choice:
    """Create a new choice in the database."""
    db_choice = models.Choice(
        choice_text=choice.choice_text,
        is_correct=choice.is_correct,
        question_id=choice.question_id
    )
    db.add(db_choice)
    db.commit()
    db.refresh(db_choice)
    return db_choice


def get_all_choices(db: Session) -> list[models.Choice]:
    """Retrieve all choices from the database."""
    return db.query(models.Choice).all()


def get_choice_by_id(db: Session, choice_id: int) -> models.Choice | None:
    """Retrieve a single choice by its ID. Returns None if not found."""
    return db.query(models.Choice).filter(models.Choice.id == choice_id).first()


def update_choice(
    db: Session, choice_id: int, choice_data: schemas.ChoiceUpdate
) -> models.Choice | None:
    """Update an existing choice. Returns None if the choice does not exist."""
    db_choice = get_choice_by_id(db, choice_id)
    if db_choice is None:
        return None

    db_choice.choice_text = choice_data.choice_text
    db_choice.is_correct = choice_data.is_correct
    db_choice.question_id = choice_data.question_id
    db.commit()
    db.refresh(db_choice)
    return db_choice


def delete_choice(db: Session, choice_id: int) -> models.Choice | None:
    """Delete a choice. Returns None if the choice does not exist."""
    db_choice = get_choice_by_id(db, choice_id)
    if db_choice is None:
        return None

    db.delete(db_choice)
    db.commit()
    return db_choice
