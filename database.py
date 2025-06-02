from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import os

def get_database_engine():
    # Try the environment variable first (if set)
    env_db_url = os.getenv("SQLALCHEMY_DATABASE_URL")
    fallback_db_url = "postgresql://postgres:password@localhost:5432/dev.scambet"

    if env_db_url:
        try:
            # Test if the connection works (3s timeout)
            test_engine = create_engine(env_db_url, connect_args={'connect_timeout': 3}, echo=True)
            with test_engine.connect() as conn:
                print("✅ Connected to ENV database")
                return test_engine  # Return working engine
        except OperationalError as e:
            print(f"❌ Failed to connect to ENV database: {e}")
    
    # Fallback to local PostgreSQL if env fails or is not set
    try:
        test_engine = create_engine(fallback_db_url, connect_args={'connect_timeout': 3}, echo=True)
        with test_engine.connect() as conn:
            print("✅ Falling back to LOCAL database")
            return test_engine
    except OperationalError as e:
        raise RuntimeError("❌ Failed to connect to both ENV and LOCAL databases") from e

# Get the working engine (auto-fallback)
engine = get_database_engine()

# Create session (SQLModel-compatible)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session  # Ensures SQLModel compatibility
)