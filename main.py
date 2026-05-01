# main.py
# FastAPI application entry point
# Exposes a REST API for uploading media files and returning AI transcriptions

import shutil
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, UploadFile, File, Query
from sqlmodel import Session
from database import init_db, get_session
from models import MediaTask
from services import transcribe_audio

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler — runs setup code before the app starts accepting requests.
    Initializes the MySQL database tables on startup.
    """
    print("Connecting to MySQL and building tables...")
    init_db()
    yield  # App runs here
    print("Shutting down...")

# Initialize the FastAPI app with the lifespan handler
app = FastAPI(
    lifespan=lifespan,
    title="Media Transcription API",
    description="AI-powered audio and video transcription using OpenAI Whisper",
    version="1.0.0"
)

@app.get("/")
def home():
    """Health check endpoint — confirms the API is running and connected."""
    return {"status": "Media Automation API is online and connected to MySQL!"}

@app.post("/upload/")
async def upload_media(
    file: UploadFile = File(...),            # The uploaded audio/video file (required)
    task: str = Query(default="transcribe"), # 'transcribe' or 'translate'
    session: Session = Depends(get_session)  # DB session injected by FastAPI
):
    """
    Main transcription endpoint.

    Accepts a media file upload and returns the AI-generated transcription.

    Workflow:
        1. Save uploaded file temporarily to disk
        2. Create a database record with status 'processing'
        3. Send file to Whisper AI for transcription/translation
        4. Update the database record with the completed text
        5. Delete the temporary file from disk
        6. Return the transcription as a JSON response
    """

    # 1. Save the uploaded file to a temporary path on disk
    # Whisper requires a real file path, not an in-memory stream
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Create an initial DB record to track this job
    new_task = MediaTask(filename=file.filename, status="processing")
    session.add(new_task)
    session.commit()

    # 3. Run Whisper AI — this may take several seconds depending on file length
    print(f"Sending {file_location} to Whisper AI... (task={task})")
    transcribed_text = transcribe_audio(file_location, task=task)

    # 4. Update the DB record with the transcription result
    new_task.transcription_text = transcribed_text
    new_task.status = "completed"
    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    # 5. Remove the temporary file to free up disk space
    os.remove(file_location)

    # 6. Return the result as JSON
    return {
        "message": "Transcription complete!",
        "filename": new_task.filename,
        "task": task,
        "text": new_task.transcription_text
    }