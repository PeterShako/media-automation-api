import streamlit as st
import requests

st.set_page_config(
    page_title="Media Transcription Studio",
    page_icon="🎙️",
    layout="centered"
)

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
        .stButton>button:hover {
            background-color: #17a349;
        }
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

# Header
st.markdown("# 🎙️ Shako Transcription Studio")
st.markdown("Upload any audio or video file and get an instant AI-powered transcription.")
st.divider()

# Settings
col1, col2 = st.columns(2)
with col1:
    task = st.selectbox(
        "🌐 Output Mode",
        ["Transcribe (keep original language)", "Translate (to English)"]
    )
with col2:
    st.markdown("**Supported formats**")
    st.caption("WAV · MP3 · MP4 · M4A · OGG · FLAC")

st.divider()

# File uploader
audio_file = st.file_uploader(
    "📂 Drop your file here",
    type=["wav", "mp3", "mp4", "m4a", "ogg", "flac"]
)

if audio_file:
    st.audio(audio_file)
    st.caption(f"📄 File: `{audio_file.name}`")

    if st.button("Start Transcription"):
        with st.spinner("Whisper AI is transcribing... please wait ⏳"):
            try:
                files = {"file": (audio_file.name, audio_file, audio_file.type)}
                params = {"task": "translate" if "Translate" in task else "transcribe"}
                response = requests.post(
                    "http://127.0.0.1:8000/upload/",
                    files=files,
                    params=params
                )

                if response.status_code == 200:
                    data = response.json()
                    transcription = data.get("text", "")

                    st.success("✅ Transcription complete!")
                    st.divider()
                    st.markdown("### 📝 Result")
                    st.markdown(
                        f'<div class="result-box">{transcription}</div>',
                        unsafe_allow_html=True
                    )
                    st.divider()

                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="⬇️ Download as .txt",
                            data=transcription,
                            file_name=f"{audio_file.name}_transcription.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    with col2:
                        st.metric("Characters", len(transcription))

                else:
                    st.error(f"API Error {response.status_code}: {response.text}")

            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot reach API. Make sure uvicorn is running on port 8000.")