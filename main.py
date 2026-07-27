import yt_dlp
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel

app = FastAPI(title="ClipScale API")

class ClipRequest(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"message": "ClipScale backend is live!"}

@app.post("/api/v1/process")
async def process_video(request: ClipRequest, background_tasks: BackgroundTasks):
    if not request.url:
        raise HTTPException(status_code=400, detail="URL is required")
    
    background_tasks.add_task(run_video_pipeline, request.url)
    
    return {
        "status": "processing",
        "message": "Video ingestion started successfully.",
        "url": request.url
    }

def run_video_pipeline(url: str):
    print(f"Processing video from: {url}")
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("Video download completed successfully.")
