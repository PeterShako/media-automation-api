# database.py
# Handles MySQL database connection and session management
# Uses PyMySQL driver with cryptography package for SHA2 auth (MySQL 8 requirement)

from sqlmodel import create_engine, Session
from models import SQLModel
import urllib.parse

# URL-encode the password to safely handle special characters like @ and #
password = urllib.parse.quote_plus("Qwer4126@tf2787")

# MySQL connection string — format: driver://user:password@host:port/database
DATABASE_URL = f"mysql+pymysql://root:{password}@localhost:3306/media_api"

# Create the engine — echo=True logs all SQL queries to terminal (useful for debugging)
# Set echo=False in production to reduce noise
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    """
    Creates all tables defined in SQLModel metadata if they don't already exist.
    Called once at application startup via the FastAPI lifespan event.
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    FastAPI dependency that provides a database session per request.
    The 'with' block ensures the session is properly closed after each request,
    even if an error occurs.
    """
    with Session(engine) as session:
        yield session