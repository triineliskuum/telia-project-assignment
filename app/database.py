"""
This file is responsible for database configuration.

It creates:
- database connection (engine)
- session factory (SessionLocal)
- Base class for SQLAlchemy models
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL (local file-based database)
DATABASE_URL = "sqlite:///./project_assignment.db"

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} # needed for SQLite
)

# Session factory for database operations
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all models (tables)
Base = declarative_base()