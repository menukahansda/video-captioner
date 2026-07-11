# Video Captioner
AI-powered video captioning tool that generates captions in four distinct styles: formal, sarcastic, humorous tech, and humorous non-tech.

## Table of Contents
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Authors](#authors)

## Project Structure
```text
video-captioner/
│                        
├── .gitignore
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── README.md
│   ├── requirements.txt
│   ├── .env.example            
│   ├── .gitignore
│   │
│   ├── config/
│   │   └── settings.py          
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py      
│   │   ├── schemas.py         
│   │   ├── routes/
│   │   └── services/         
│   │
│   ├── src/
│   │   ├── __init__.py
│   │   │
│   │   ├── preprocessing/
│   │   │   ├── __init__.py
│   │   │   ├── validate.py
│   │   │   ├── audio_extractor.py
│   │   │   ├── keyframe_extractor.py
│   │   │   └── audio_transcribe.py
│   │   │
│   │   ├── captioning/
│   │   │   ├── __init__.py
│   │   │   ├── llm_client.py
│   │   │   ├── gemini_backend.py
│   │   │   ├── local_backend.py
│   │   │   └── prompts.py
│   │   │
│   │   ├── merge.py
│   │   ├── pipeline.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── cleanup.py
│   │       └── logging.py
│   │
│   ├── data/
│   │   ├── uploads/
│   │   ├── frames/
│   │   ├── audio/
│   │   └── outputs/
│   │
│   ├── scripts/
│   │   ├── run_single.py
│   │   └── run_batch.py
│   │
│   └── tests/
│       ├── test_keyframe_extractor.py
│       ├── test_audio_transcribe.py
│       └── test_pipeline.py
│
└── frontend/
    ├── public/
    │   └── favicon.svg
    ├── src/
    │   ├── components/
    │   │   └── FileUploader.jsx
    │   ├── utils/
    │   │   └── userId.js
    │   ├── App.jsx
    │   ├── index.css
    │   ├── App.css
    │   └── main.jsx
    ├── .env.example
    ├── package.json
    ├── vite.config.js
    ├── eslint.config.js
    └── index.html

```

## Requirements

- Python 3.13 (tested with Python 3.13.14)
- Node.js (includes npm)
- FFmpeg (must be installed and available in your system PATH)


## Installation
### Root
Install the root development dependencies.

```bash
npm install
```

### Backend

```bash
# from root
cd backend

python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# Git Bash
source venv/Scripts/activate

pip install -r requirements.txt
```

### Frontend

```bash
# from root
cd frontend
npm install
```


## Usage
### Run the full application

```bash
npm run dev
```

### Run backend as CLI

```bash
# from root
cd backend

```

```bash
python scripts/run_single.py path/to/video.mp4  #single video
python scripts/run_batch.py path/to/video1.mp4 path/to/video2.mp4  #multiple videos
```


## Authors
- [Menuka Hansda](https://github.com/menukahansda/) & [Shreya](https://github.com/Shree0l0l)