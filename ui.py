# ui.py
# Streamlit frontend for the Media Transcription API
# Provides a clean dark-themed UI for uploading files and viewing transcriptions
# Requires the FastAPI backend (main.py) to be running on port 8000

import streamlit as st
import requests

# Configure the Streamlit page — must be the first Streamlit call
st.set_page_config(
    page_title="Media Transcription Studio",
    page_icon="🎙️",
    layout="centered"
)

# Custom CSS — dark background with green (#1DB954) accent colors
st.markdown("""
    <style>
        .main { background-color: #0e1117; }
        .stButton>button {
            width: 100%;
            background-color: #1DB954;
            color: white;
            font-size: 18px;
            padding: 12px;
            border-radius: 10px;
            border: none;
        }
        .stButton>button:hover { background-color: #17a349; }
        .result-box {
            background-color: #1e1e2e;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #1DB954;
            color: white;
            font-size: 15px;
            line-height: 1.8;
        }
        h1 { color: #1DB954 !important; }
    </style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown("# 🎙️ Shako Transcription Studio")
st.markdown("Upload any audio or video file and get an instant AI-powered transcription.")
st.divider()

# ── Settings Row ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    # Dropdown to select transcription mode
    task = st.selectbox(
        "🌐 Output Mode",
        ["Transcribe (keep original language)", "Translate (to English)"]
    )
with col2:
    st.markdown("**Supported formats**")
    st.caption("WAV · MP3 · MP4 · M4A · OGG · FLAC")

st.divider()

# ── File Uploader ─────────────────────────────────────────────────────────────
audio_file = st.file_uploader(
    "📂 Drop your file here",
    type=["wav", "mp3", "mp4", "m4a", "ogg", "flac"]
)

if audio_file:
    # Show a preview audio player for the uploaded file
    st.audio(audio_file)
    st.caption(f"📄 File: `{audio_file.name}`")

    # ── Transcription Button ──────────────────────────────────────────────────
    if st.button("🚀 Start Transcription"):
        with st.spinner("Whisper AI is transcribing... please wait ⏳"):
            try:
                # Prepare the file for multipart form upload to FastAPI
                files = {"file": (audio_file.name, audio_file, audio_file.type)}

                # Map UI selection to API task parameter
                params = {"task": "translate" if "Translate" in task else "transcribe"}

                # Send POST request to the FastAPI /upload/ endpoint
                response = requests.post(
                    "http://127.0.0.1:8000/upload/",
                    files=files,
                    params=params
                )

                # ── Handle Success ────────────────────────────────────────────
                if response.status_code == 200:
                    data = response.json()
                    transcription = data.get("text", "")

                    st.success("✅ Transcription complete!")
                    st.divider()
                    st.markdown("### 📝 Result")

                    # Display transcription in a styled dark box
                    st.markdown(
                        f'<div class="result-box">{transcription}</div>',
                        unsafe_allow_html=True
                    )
                    st.divider()

                    # ── Download + Stats Row ──────────────────────────────────
                    col1, col2 = st.columns(2)
                    with col1:
                        # Allow user to download the transcription as a .txt file
                        st.download_button(
                            label="⬇️ Download as .txt",
                            data=transcription,
                            file_name=f"{audio_file.name}_transcription.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with col2:
                        # Show character count as a quick quality indicator
                        st.metric("Characters", len(transcription))

                # ── Handle API Errors ─────────────────────────────────────────
                else:
                    st.error(f"API Error {response.status_code}: {response.text}")

            # ── Handle Connection Error (API not running) ─────────────────────
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot reach API. Make sure uvicorn is running on port 8000.")