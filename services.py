import whisper

def transcribe_audio(file_path: str, task: str = "transcribe"):
    
    print(f"Loading AI model and transcribing {file_path}...")
    
    # We use 'base' for testing speed. 
    model = whisper.load_model("medium")
    
    # Run the transcription
    result = model.transcribe(file_path, task=task)
    return result["text"]
