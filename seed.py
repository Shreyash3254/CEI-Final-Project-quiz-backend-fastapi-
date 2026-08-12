"""
Seed Script — Inserts sample quiz data into the database.

Run this script to populate the database with example questions and choices
for testing purposes.

Usage:
    python seed.py
"""

from app.database import SessionLocal, engine, Base
from app.models import Question, Choice


def seed_data():
    """Insert sample quiz questions and choices into the database."""

    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if data already exists to avoid duplicates
        existing = db.query(Question).count()
        if existing > 0:
            print(f"Database already contains {existing} question(s). Skipping seed.")
            return

        # Sample quiz data: list of (question_text, category, choices)
        # Each choice is (choice_text, is_correct)
        sample_data = [
            {
                "question_text": "What is the capital of France?",
                "category": "General Knowledge",
                "choices": [
                    ("Paris", True),
                    ("London", False),
                    ("Berlin", False),
                    ("Madrid", False),
                ],
            },
            {
                "question_text": "Which programming language is known as the 'language of the web'?",
                "category": "Programming",
                "choices": [
                    ("Python", False),
                    ("JavaScript", True),
                    ("C++", False),
                    ("Java", False),
                ],
            },
            {
                "question_text": "What is the value of Pi rounded to two decimal places?",
                "category": "Mathematics",
                "choices": [
                    ("3.14", True),
                    ("3.15", False),
                    ("2.14", False),
                    ("3.41", False),
                ],
            },
            {
                "question_text": "What does CPU stand for?",
                "category": "General Knowledge",
                "choices": [
                    ("Central Processing Unit", True),
                    ("Central Program Utility", False),
                    ("Computer Personal Unit", False),
                    ("Central Processor Unifier", False),
                ],
            },
            {
                "question_text": "Which Python library is commonly used for data manipulation?",
                "category": "Data Science",
                "choices": [
                    ("NumPy", False),
                    ("Pandas", True),
                    ("Flask", False),
                    ("Django", False),
                ],
            },
            {
                "question_text": "What is the square root of 144?",
                "category": "Mathematics",
                "choices": [
                    ("10", False),
                    ("11", False),
                    ("12", True),
                    ("14", False),
                ],
            },
            {
                "question_text": "Which keyword is used to define a function in Python?",
                "category": "Programming",
                "choices": [
                    ("func", False),
                    ("define", False),
                    ("def", True),
                    ("function", False),
                ],
            },
            {
                "question_text": "What is the full form of HTML?",
                "category": "Programming",
                "choices": [
                    ("Hyper Text Markup Language", True),
                    ("High Text Machine Language", False),
                    ("Hyper Tabular Markup Language", False),
                    ("Hyper Text Managing Language", False),
                ],
            },
            {
                "question_text": "If a train travels 60 km in 1 hour, how far will it travel in 5 hours?",
                "category": "Aptitude",
                "choices": [
                    ("200 km", False),
                    ("300 km", True),
                    ("350 km", False),
                    ("400 km", False),
                ],
            },
            {
                "question_text": "Which of the following is a supervised learning algorithm?",
                "category": "Data Science",
                "choices": [
                    ("K-Means Clustering", False),
                    ("Linear Regression", True),
                    ("PCA", False),
                    ("DBSCAN", False),
                ],
            },
        ]

        # Insert each question and its choices
        for item in sample_data:
            question = Question(
                question_text=item["question_text"],
                category=item["category"],
            )
            db.add(question)
            db.flush()  # Flush to get the question ID before adding choices

            for choice_text, is_correct in item["choices"]:
                choice = Choice(
                    choice_text=choice_text,
                    is_correct=is_correct,
                    question_id=question.id,
                )
                db.add(choice)

        db.commit()
        print(f"Successfully seeded {len(sample_data)} questions with choices.")

    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
