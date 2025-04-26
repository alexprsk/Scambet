from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.orm import sessionmaker

# SQLite (or use your PostgreSQL URL)
SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=True  # Optional - shows SQL queries in console
)

# This creates the proper Session class for SQLModel
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session  # This is the key difference
)