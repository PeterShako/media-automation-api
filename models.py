from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Text
from typing import Optional
from datetime import datetime, timezone

class MediaTask(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    status: str = Field(default="pending")
    transcription_text: Optional[str] = Field(
        default=None, sa_column=Column(Text)
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))