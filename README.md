# Video Captioner
AI-powered video captioning tool that generates captions in four distinct styles: formal, sarcastic, humorous tech, and humorous non-tech.

## Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Authors](#authors)

## Project Structure
```text
video-captioner/
│
├── docker-compose.yml                          
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
│   │   │   ├── fireworks_backend.py
│   │   │   ├── local_backend.py
│   │   │   └── prompts.py
│   │   │
│   │   ├── merge.py
│   │   ├── pipeline.py
│   │   └── utils/
│   │       ├── __init__.py
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
└── frontend

```
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

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### Frontend

```bash
# from root
cd frontend
npm install
```


## Usage
### Run the complete application

```bash
npm run dev
```

### Run backend only

```bash
# from root
cd backend
# Activate virtual environment first
python scripts/run_batch.py data/uploads/       #multiple videos
python scripts/run_single.py                    #single video
```


## Authors
- [Menuka Hansda](https://github.com/menukahansda/) & [Shreya](https://github.com/Shree0l0l)