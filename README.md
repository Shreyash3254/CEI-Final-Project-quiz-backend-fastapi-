# Quiz Backend Management API using FastAPI

## Project Overview

A RESTful backend application for managing quiz questions and answer choices, built as a final project for the **Celebal Excellence Internship (CEI) Program 2026!**. The API supports full CRUD operations on quiz questions and their associated answer choices, with proper input validation and relational database management.

## Problem Statement

Develop a backend system that allows users to create, read, update, and delete quiz questions along with their associated answer choices. The system must maintain a proper relationship between questions and choices, validate all input data, and handle errors gracefully.

“The Quiz Backend Management System is a RESTful API built using FastAPI to manage quiz questions and choices. It uses SQLAlchemy for database operations and Pydantic for validation. The system supports CRUD operations, maintains relationships between questions and answers, and enables efficient data storage and retrieval for quiz-based applications.”


## Objectives

- Build a RESTful API using FastAPI for managing quiz data
- Implement full CRUD operations for both Questions and Choices
- Maintain a one-to-many relationship between Questions and Choices
- Validate all API inputs using Pydantic schemas
- Manage database operations using SQLAlchemy ORM
- Provide automatic interactive API documentation
- Handle errors with appropriate HTTP status codes

## Technology Stack

| Technology   | Purpose                        |
|-------------|-------------------------------|
| Python 3    | Programming language           |
| FastAPI     | Web framework for building APIs |
| SQLAlchemy  | ORM for database operations     |
| Pydantic    | Data validation and serialization |
| SQLite      | Lightweight relational database  |
| Uvicorn     | ASGI server to run the application |

## System Architecture

```
Client Request (HTTP)
        ↓
  FastAPI Routes (app/main.py)
        ↓
  Business Logic / CRUD (app/crud.py)
        ↓
  SQLAlchemy ORM (app/models.py)
        ↓
  SQLite Database (quiz.db)
```

## Database Design

### Question Table

| Field          | Type    | Description                    |
|---------------|---------|-------------------------------|
| `id`          | Integer | Primary Key, auto-incremented  |
| `question_text` | String  | The quiz question text (required) |
| `category`    | String  | Optional category for the question |

### Choice Table

| Field          | Type    | Description                              |
|---------------|---------|----------------------------------------|
| `id`          | Integer | Primary Key, auto-incremented            |
| `choice_text` | String  | The answer choice text (required)        |
| `is_correct`  | Boolean | Whether this choice is correct (required) |
| `question_id` | Integer | Foreign Key referencing Question table    |

### Question–Choice Relationship

- **One Question → Many Choices**: Each question can have multiple answer choices.
- **Cascade Delete**: When a question is deleted, all its associated choices are automatically deleted.
- Implemented using SQLAlchemy's `relationship()` with `cascade="all, delete-orphan"`.

```
┌──────────────┐         ┌──────────────┐
│   Question   │         │    Choice    │
├──────────────┤         ├──────────────┤
│ id (PK)      │───1:N──▶│ id (PK)      │
│ question_text│         │ choice_text  │
│ category     │         │ is_correct   │
└──────────────┘         │ question_id  │
                         │   (FK)       │
                         └──────────────┘
```

## API Endpoints

### Question Endpoints

| Method   | Endpoint              | Description                                      |
|---------|-----------------------|--------------------------------------------------|
| `POST`  | `/questions`          | Create a new quiz question                        |
| `GET`   | `/questions`          | Retrieve all questions with their choices          |
| `GET`   | `/questions/{id}`     | Retrieve a specific question by ID                 |
| `PUT`   | `/questions/{id}`     | Update an existing question                        |
| `DELETE`| `/questions/{id}`     | Delete a question and its associated choices       |

### Choice Endpoints

| Method   | Endpoint              | Description                                      |
|---------|-----------------------|--------------------------------------------------|
| `POST`  | `/choices`            | Add an answer choice to a question                 |
| `GET`   | `/choices`            | Retrieve all answer choices                        |
| `PUT`   | `/choices/{id}`       | Update an existing choice                          |
| `DELETE`| `/choices/{id}`       | Delete an answer choice                            |

## Project Structure

```
quiz-backend-fastapi/
│
├── app/
│   ├── __init__.py       # Package initializer
│   ├── main.py           # FastAPI app and API routes
│   ├── database.py       # Database configuration and session management
│   ├── models.py         # SQLAlchemy ORM models (Question, Choice)
│   ├── schemas.py        # Pydantic request/response schemas
│   └── crud.py           # CRUD database operations
│
├── seed.py               # Script to insert sample quiz data
├── requirements.txt      # Python dependencies
├── .gitignore            # Git ignore rules
└── README.md             # Project documentation
```

### File Responsibilities

| File           | Purpose                                                  |
|---------------|----------------------------------------------------------|
| `main.py`     | FastAPI application, API route definitions, app startup   |
| `database.py` | SQLite config, SQLAlchemy engine, session dependency      |
| `models.py`   | Question and Choice ORM models with relationship          |
| `schemas.py`  | Pydantic models for request validation and response       |
| `crud.py`     | Create, Read, Update, Delete database operations          |
| `seed.py`     | Insert sample quiz questions and choices                  |

## Installation Instructions

### Prerequisites

- Python 3.10 or higher installed on your system

### Steps

1. **Clone or download the project**

   ```bash
   cd quiz-backend-fastapi
   ```

2. **Create a virtual environment**

   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**

   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Application

1. **Start the FastAPI server**

   ```bash
   uvicorn app.main:app --reload
   ```

   The server will start at `http://127.0.0.1:8000`.

2. **Access the API documentation**

   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## How to Seed Sample Data

Run the seed script to populate the database with 10 sample quiz questions across 5 categories:

```bash
python seed.py
```

Sample categories include: General Knowledge, Programming, Mathematics, Data Science, and Aptitude.

Each question comes with 4 answer choices, with exactly one correct answer.

> **Note:** The seed script checks if data already exists and will not create duplicates.

## Swagger Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI** at `/docs` — Interactive interface to test all endpoints directly from the browser.
- **ReDoc** at `/redoc` — Clean, readable API reference documentation.

Both show all endpoints, request/response schemas, and example data.

## API Testing Examples

### Create a Question

```bash
curl -X POST http://127.0.0.1:8000/questions \
  -H "Content-Type: application/json" \
  -d '{"question_text": "What is Python?", "category": "Programming"}'
```

**Response** (201 Created):
```json
{
  "id": 1,
  "question_text": "What is Python?",
  "category": "Programming",
  "choices": []
}
```

### Add a Choice to a Question

```bash
curl -X POST http://127.0.0.1:8000/choices \
  -H "Content-Type: application/json" \
  -d '{"choice_text": "A programming language", "is_correct": true, "question_id": 1}'
```

**Response** (201 Created):
```json
{
  "id": 1,
  "choice_text": "A programming language",
  "is_correct": true,
  "question_id": 1
}
```

### Get All Questions

```bash
curl http://127.0.0.1:8000/questions
```

### Get a Specific Question

```bash
curl http://127.0.0.1:8000/questions/1
```

### Update a Question

```bash
curl -X PUT http://127.0.0.1:8000/questions/1 \
  -H "Content-Type: application/json" \
  -d '{"question_text": "What is Python programming?", "category": "Programming"}'
```

### Delete a Question (Cascade Deletes Choices)

```bash
curl -X DELETE http://127.0.0.1:8000/questions/1
```

### Get All Choices

```bash
curl http://127.0.0.1:8000/choices
```

### Update a Choice

```bash
curl -X PUT http://127.0.0.1:8000/choices/1 \
  -H "Content-Type: application/json" \
  -d '{"choice_text": "A high-level language", "is_correct": true, "question_id": 1}'
```

### Delete a Choice

```bash
curl -X DELETE http://127.0.0.1:8000/choices/1
```

## Error Handling

The API returns appropriate HTTP error responses:

| Status Code | Description                          | When                                          |
|------------|--------------------------------------|-----------------------------------------------|
| `201`      | Created                              | Resource successfully created                  |
| `200`      | OK                                   | Request successful                             |
| `404`      | Not Found                            | Question or Choice ID does not exist           |
| `422`      | Unprocessable Entity (Validation)    | Invalid request body or incorrect data types   |

### Example 404 Response

```json
{
  "detail": "Question not found"
}
```

### Example 422 Response (Missing Required Field)

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "question_text"],
      "msg": "Field required",
      "input": {}
    }
  ]
}
```

## Expected Learning Outcomes

Through this project, the following skills and concepts are demonstrated:

1. **FastAPI Framework** — Building RESTful APIs with automatic documentation
2. **Pydantic Validation** — Request/response data validation and serialization
3. **SQLAlchemy ORM** — Database modeling, relationships, and CRUD operations
4. **Database Design** — Relational tables with foreign keys and cascade behavior
5. **Error Handling** — Proper HTTP status codes and error messages
6. **Project Structure** — Clean, modular, and maintainable code organization
7. **API Design** — RESTful conventions and best practices
