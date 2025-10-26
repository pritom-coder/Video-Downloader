from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  
from pydantic import BaseModel
import yt_dlp
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()
DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", "downloads")
DEBUG = os.getenv("DEBUG", "False") == "True"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class VideoRequest(BaseModel):
    url: str

# Route define
@app.post("/download")
def download_video(request: VideoRequest):
    url = request.url
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'noplaylist': True,  
    }


    if DEBUG:
        print(f"[DEBUG] Downloading from URL: {url}")
        print(f"[DEBUG] Saving to folder: {DOWNLOAD_DIR}")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if DEBUG:
                print(f"[DEBUG] Download completed: {filename}")
        return {"title": info.get('title'), "filename": filename}
    except Exception as e:
        if DEBUG:
            print(f"[DEBUG] Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
