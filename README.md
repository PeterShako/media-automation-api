# 🎙️ Media Transcription API

> An AI-powered audio and video transcription system built with FastAPI, OpenAI Whisper, MySQL, and Streamlit.

---

## 📖 Description

Media Transcription API is a full-stack AI application that accepts audio and video file uploads, transcribes them using OpenAI's Whisper model, stores the results in a MySQL database, and presents them through a clean, dark-themed Streamlit UI. It supports transcription in 90+ languages including Swahili, and can optionally translate any language to English automatically.

Built as part of the **Foundations: Generative AI for Developers** course at Moringa School.

---

## ✨ Features

- 🎵 Upload audio and video files (WAV, MP3, MP4, M4A, OGG, FLAC)
- 🤖 AI transcription powered by OpenAI Whisper
- 🌍 Supports 90+ languages including Swahili
- 🔄 Toggle between **Transcribe** (keep original language) and **Translate** (to English)
- 💾 Saves all transcriptions to a MySQL database
- ⬇️ Download transcription results as `.txt` files
- 🖥️ Clean, dark-themed Streamlit UI
- 📡 RESTful API with auto-generated Swagger docs

---

## 🛠️ Technologies Used

| Layer | Technology |
|-------|------------|
| Backend API | FastAPI (Python) |
| AI Transcription | OpenAI Whisper |
| Database | MySQL 8 |
| ORM | SQLModel + SQLAlchemy |
| Frontend UI | Streamlit |
| Server | Uvicorn (ASGI) |
| Auth Driver | PyMySQL + cryptography |

---

## 📋 Prerequisites

Before running this project, make sure you have the following installed:

- **Python 3.10+** — [python.org](https://python.org)
- **MySQL Server 8.0+** — [dev.mysql.com](https://dev.mysql.com/downloads/)
- **MySQL Workbench** — [dev.mysql.com/downloads](https://dev.mysql.com/downloads/workbench/)
- **FFmpeg** (required by Whisper) — [ffmpeg.org](https://ffmpeg.org) or [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) for Windows

> ⚠️ **FFmpeg must be added to your system PATH** for Whisper to process audio files.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/PeterShako/media-automation-api.git
cd media-automation-api
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

**Windows (PowerShell):**
```powershell
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (.\venv\Scripts\Activate.ps1)
```

**Mac / Linux:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install fastapi uvicorn sqlmodel pymysql cryptography openai-whisper streamlit requests
```

### 5. Set Up the Database

Open MySQL Workbench and run:

```sql
CREATE DATABASE IF NOT EXISTS media_api;
USE media_api;
```

> The `mediatask` table is created automatically on first run. After first run, execute this to support long transcriptions:

```sql
ALTER TABLE mediatask MODIFY COLUMN transcription_text TEXT;
```

### 6. Configure Database Credentials

Open `database.py` and update the password to match your MySQL root password:

```python
password = urllib.parse.quote_plus("YOUR_MYSQL_PASSWORD_HERE")
```

---

## 🚀 Usage

You need **two terminals** open simultaneously, both with the venv activated.

### Terminal 1 — Start the API

```bash
uvicorn main:app --reload
```

API available at: `http://127.0.0.1:8000`  
Swagger docs at: `http://127.0.0.1:8000/docs`

### Terminal 2 — Start the UI

```bash
streamlit run ui.py
```

UI opens automatically at: `http://localhost:8501`

### Using the UI

1. Open `http://localhost:8501` in your browser
2. Select **Output Mode**: Transcribe or Translate to English
3. Upload an audio/video file
4. Click **Start Transcription**
5. View and download the result as a `.txt` file

---

## 📁 Project Structure

```
media-automation-api/
├── main.py          # FastAPI app and /upload/ endpoint
├── models.py        # SQLModel database schema (MediaTask)
├── database.py      # MySQL engine, session, and init_db()
├── services.py      # Whisper AI transcription logic
├── ui.py            # Streamlit frontend UI
├── .gitignore       # Excludes venv, pycache, temp files
└── README.md        # This file
```

---

## 📡 API Endpoints

| Method | Endpoint | Parameters | Description |
|--------|----------|------------|-------------|
| `GET` | `/` | None | Health check — returns API status |
| `POST` | `/upload/` | `file` (form-data), `task` (query) | Upload and transcribe a media file |

### Example API Request

```bash
curl -X POST "http://127.0.0.1:8000/upload/?task=transcribe" \
  -F "file=@your_audio.wav"
```

### Example Response

```json
{
  "message": "Transcription complete!",
  "filename": "your_audio.wav",
  "task": "transcribe",
  "text": "Welcome to this course on Insurance and Law..."
}
```

---

## 🌍 Language Support

Whisper supports 90+ languages out of the box.

- **Transcribe mode** — output stays in the original spoken language (e.g., Swahili stays Swahili)
- **Translate mode** — converts any language to English automatically

To improve accuracy for non-English languages, change the model size in `services.py`:

```python
model = whisper.load_model("small")   # better accuracy, slightly slower
model = whisper.load_model("medium")  # best accuracy, slowest
```

---

## 🔧 Configuration Options

| Setting | Location | Default | Options |
|---------|----------|---------|---------|
| Whisper model size | `services.py` | `base` | `tiny`, `base`, `small`, `medium`, `large` |
| Task mode | `ui.py` / API query | `transcribe` | `transcribe`, `translate` |
| Database name | `database.py` | `media_api` | Any valid MySQL DB name |
| API port | terminal command | `8000` | `--port XXXX` flag on uvicorn |
| UI port | terminal command | `8501` | `--server.port XXXX` flag on streamlit |

---

## 🐛 Troubleshooting

### `cryptography` package error on startup
```bash
pip install cryptography
```

### `Data too long for column 'transcription_text'`
Run in MySQL Workbench:
```sql
USE media_api; 
ALTER TABLE mediatask MODIFY COLUMN transcription_text TEXT;
```

### `Cannot connect to API` error in Streamlit UI
Make sure uvicorn is running in Terminal 1. Both the API and UI must be running at the same time.

### Streamlit/requests import warnings in VS Code
Press `Ctrl+Shift+P` → `Python: Select Interpreter` → choose the venv Python:
`.\venv\Scripts\python.exe`

### `index.lock` git error
```powershell
Remove-Item .git/index.lock
```

### FFmpeg not found by Whisper
Download FFmpeg from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/), extract it, and add the `bin/` folder to your Windows PATH environment variable. Restart PowerShell after.

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m "Add your feature"`
4. Push to your fork: `git push origin feature/your-feature-name`
5. Open a Pull Request on GitHub

Please keep code clean, commented, and consistent with the existing style.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Peter Shako**  
Moringa School — Generative AI for Developers, 2026  
GitHub: [@PeterShako](https://github.com/PeterShako)
