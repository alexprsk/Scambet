from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from dotenv import load_dotenv
import os

load_dotenv("prod.env")

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

def get_database_engine():
    try:
        test_engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            connect_args={"connect_timeout": 3},
            echo=True
        )
        with test_engine.connect() as conn:
            print("✅ Connected to database")
        return test_engine
    except OperationalError as e:
        raise RuntimeError(f"❌ Could not connect to the database at {SQLALCHEMY_DATABASE_URL}") from e

engine = get_database_engine()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_= Session  # Ensures SQLModel compatibility
)