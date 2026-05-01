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
    print("Connecting to MySQL and building tables...")
    init_db()
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"status": "Media Automation API is online and connected to MySQL!"}

@app.post("/upload/")
async def upload_media(
    file: UploadFile = File(...),
    task: str = Query(default="transcribe"),
    session: Session = Depends(get_session)
):
    # 1. Save the file locally
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 2. Create the initial database record
    new_task = MediaTask(filename=file.filename, status="processing")
    session.add(new_task)
    session.commit()

    # 3. RUN THE AI TRANSCRIPTION
    print(f"Sending {file_location} to Whisper AI... (task={task})")
    transcribed_text = transcribe_audio(file_location, task=task)

    # 4. Update the database with the final text
    new_task.transcription_text = transcribed_text
    new_task.status = "completed"
    session.add(new_task)
    session.commit()
    session.refresh(new_task)

    # 5. Clean up the temp file
    os.remove(file_location)

    return {
        "message": "Transcription complete!",
        "filename": new_task.filename,
        "task": task,
        "text": new_task.transcription_text
    }