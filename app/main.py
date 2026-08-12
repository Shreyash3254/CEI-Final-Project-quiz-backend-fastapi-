"""
Quiz Backend Management API — FastAPI Application

This is the main entry point of the application.
It defines all API routes for managing quiz questions and answer choices.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import engine, get_db, Base
from app import crud, schemas

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application
app = FastAPI(
    title="Quiz Backend Management API",
    description=(
        "A RESTful backend API for managing quiz questions and answer choices. "
        "Built with FastAPI, SQLAlchemy, and SQLite as a Celebal Technologies internship project."
    ),
    version="1.0.0",
)


# ===========================================================================
# Question Endpoints
# ===========================================================================

@app.post(
    "/questions",
    response_model=schemas.QuestionResponse,
    status_code=201,
    summary="Create a new question",
    description="Creates a new quiz question with optional category.",
    tags=["Questions"],
)
def create_question(question: schemas.QuestionCreate, db: Session = Depends(get_db)):
    return crud.create_question(db, question)


@app.get(
    "/questions",
    response_model=list[schemas.QuestionResponse],
    summary="Get all questions",
    description="Returns a list of all quiz questions along with their choices.",
    tags=["Questions"],
)
def get_all_questions(db: Session = Depends(get_db)):
    return crud.get_all_questions(db)


@app.get(
    "/questions/{question_id}",
    response_model=schemas.QuestionResponse,
    summary="Get a question by ID",
    description="Returns a specific quiz question by its ID. Returns 404 if not found.",
    tags=["Questions"],
)
def get_question(question_id: int, db: Session = Depends(get_db)):
    db_question = crud.get_question_by_id(db, question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@app.put(
    "/questions/{question_id}",
    response_model=schemas.QuestionResponse,
    summary="Update a question",
    description="Updates an existing quiz question. Returns 404 if the question does not exist.",
    tags=["Questions"],
)
def update_question(
    question_id: int, question: schemas.QuestionUpdate, db: Session = Depends(get_db)
):
    db_question = crud.update_question(db, question_id, question)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@app.delete(
    "/questions/{question_id}",
    response_model=schemas.QuestionResponse,
    summary="Delete a question",
    description="Deletes a quiz question and all its associated choices (cascade delete). Returns 404 if not found.",
    tags=["Questions"],
)
def delete_question(question_id: int, db: Session = Depends(get_db)):
    db_question = crud.delete_question(db, question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


# ===========================================================================
# Choice Endpoints
# ===========================================================================

@app.post(
    "/choices",
    response_model=schemas.ChoiceResponse,
    status_code=201,
    summary="Create a new choice",
    description="Adds an answer choice to an existing question. Returns 404 if the referenced question does not exist.",
    tags=["Choices"],
)
def create_choice(choice: schemas.ChoiceCreate, db: Session = Depends(get_db)):
    # Validate that the referenced question exists
    db_question = crud.get_question_by_id(db, choice.question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return crud.create_choice(db, choice)


@app.get(
    "/choices",
    response_model=list[schemas.ChoiceResponse],
    summary="Get all choices",
    description="Returns a list of all answer choices.",
    tags=["Choices"],
)
def get_all_choices(db: Session = Depends(get_db)):
    return crud.get_all_choices(db)


@app.put(
    "/choices/{choice_id}",
    response_model=schemas.ChoiceResponse,
    summary="Update a choice",
    description="Updates an existing answer choice. Returns 404 if the choice or the referenced question does not exist.",
    tags=["Choices"],
)
def update_choice(
    choice_id: int, choice: schemas.ChoiceUpdate, db: Session = Depends(get_db)
):
    # Validate that the referenced question exists
    db_question = crud.get_question_by_id(db, choice.question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    db_choice = crud.update_choice(db, choice_id, choice)
    if db_choice is None:
        raise HTTPException(status_code=404, detail="Choice not found")
    return db_choice


@app.delete(
    "/choices/{choice_id}",
    response_model=schemas.ChoiceResponse,
    summary="Delete a choice",
    description="Deletes an answer choice. Returns 404 if the choice does not exist.",
    tags=["Choices"],
)
def delete_choice(choice_id: int, db: Session = Depends(get_db)):
    db_choice = crud.delete_choice(db, choice_id)
    if db_choice is None:
        raise HTTPException(status_code=404, detail="Choice not found")
    return db_choice
