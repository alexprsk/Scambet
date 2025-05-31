from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.orm import sessionmaker
import os

# SQLite (or use your PostgreSQL URL)
'''SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=True  # Optional - shows SQL queries in console
)'''


SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/dev.scambet"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=True )


# This creates the proper Session class for SQLModel
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session  # This is the key difference
)