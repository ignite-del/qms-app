from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os

from app.core.config import settings

# Create SQLAlchemy engine with SSL support for production
if os.environ.get('RENDER'):
    # Production configuration with SSL
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        connect_args={
            "sslmode": "require"
        }
    )
else:
    # Development configuration
    engine = create_engine(settings.DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

def get_db() -> Generator:
    """
    Dependency function to get DB session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 