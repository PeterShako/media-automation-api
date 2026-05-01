# services.py
# AI transcription logic using OpenAI Whisper
# Whisper is a multilingual speech-to-text model supporting 90+ languages

import whisper

def transcribe_audio(file_path: str, task: str = "transcribe") -> str:
    """
    Transcribes or translates an audio/video file using OpenAI Whisper.

    Args:
        file_path (str): Path to the temporary audio/video file saved on disk.
        task (str): 
            'transcribe' — output stays in the original spoken language.
            'translate'  — converts any language to English automatically.

    Returns:
        str: The full transcription or translation as a plain text string.

    Model size options (trade-off between speed and accuracy):
        'base'   — fastest, less accurate (good for testing)
        'small'  — better accuracy, slightly slower
        'medium' — best accuracy for non-English, slower (currently active)
        'large'  — highest accuracy, requires more RAM
    """
    print(f"Loading Whisper model and processing: {file_path} (task={task})")

    # Load the medium model for better multilingual accuracy (e.g. Swahili)
    model = whisper.load_model("medium")

    # Run transcription or translation based on the task parameter
    result = model.transcribe(file_path, task=task)

    return result["text"]