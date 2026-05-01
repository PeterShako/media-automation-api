# models.py
# Defines the database schema using SQLModel (combines SQLAlchemy + Pydantic)
# MediaTask represents a single transcription job stored in MySQL

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Text
from typing import Optional
from datetime import datetime, timezone

class MediaTask(SQLModel, table=True):
    """
    Database table: mediatask
    Stores each uploaded file and its transcription result.
    """

    # Auto-incremented primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Original filename of the uploaded file
    filename: str

    # Processing status: 'pending', 'processing', or 'completed'
    status: str = Field(default="pending")

    # Full transcription text — stored as TEXT type to support long outputs
    transcription_text: Optional[str] = Field(
        default=None, sa_column=Column(Text)
    )

    # Timestamp when the task was created
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))