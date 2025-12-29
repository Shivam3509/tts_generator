import os
import shutil
import uuid
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List
import asyncio

# Import refactored functions
from tts_generate import generate_audio
from video_with_text import create_full_video

app = FastAPI(title="TTS Documentary Generator")

# Create temporary directories
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mount static files
app.mount("/frontend", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")

@app.post("/generate-tts")
async def api_generate_tts(
    text: str = Form(...),
    voice: str = Form("hi-IN-MadhurNeural"),
    rate: str = Form("+30%"),
    pitch: str = Form("-5Hz"),
    bg_music: UploadFile = File(None),
    bg_volume: float = Form(0.2)
):
    try:
        bg_music_path = None
        if bg_music and bg_music.filename:
            print(f"Received BG music: {bg_music.filename}")
            bg_music_filename = f"bg_{uuid.uuid4()}_{bg_music.filename}"
            bg_music_path = os.path.join(UPLOAD_DIR, bg_music_filename)
            with open(bg_music_path, "wb") as buffer:
                shutil.copyfileobj(bg_music.file, buffer)
            print(f"Saved BG music to: {bg_music_path}")
        else:
            print("No valid BG music uploaded or filename empty.")

        filename = f"tts_{uuid.uuid4()}.mp3"
        output_path = os.path.join(OUTPUT_DIR, filename)
        await generate_audio(text, voice, rate, pitch, output_path, bg_music_path, bg_volume)
        return {
            "success": True, 
            "filename": filename, 
            "url": f"/download/{filename}",
            "bg_detected": bg_music_path is not None
        }
    except Exception as e:
        print(f"API Error in generate-tts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-video")
async def api_generate_video(
    audio_file: UploadFile = File(...),
    images: List[UploadFile] = File(...),
    video_format: str = Form("9:16")
):
    print(f"Received video generation request - Format: {video_format}, Audio: {audio_file.filename}, Images: {len(images)}")
    
    # Unique ID for this generation job
    job_id = str(uuid.uuid4())
    job_dir = os.path.join(UPLOAD_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    # Save uploaded audio file
    audio_ext = os.path.splitext(audio_file.filename)[1]
    audio_path = os.path.join(job_dir, f"audio{audio_ext}")
    with open(audio_path, "wb") as buffer:
        shutil.copyfileobj(audio_file.file, buffer)

    # Save uploaded images with original filenames to preserve order
    print(f"Received {len(images)} images in this order:")
    for i, image in enumerate(images):
        print(f"  Upload order {i+1}: {image.filename}")
        # Keep original filename
        img_path = os.path.join(job_dir, image.filename)
        with open(img_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    output_filename = f"video_{job_id}.mp4"
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    try:
        # Create video with images and audio
        create_full_video(job_dir, audio_path, output_path, video_format)
        return {"success": True, "filename": output_filename, "url": f"/download/{output_filename}"}
    except Exception as e:
        print(f"Video Generation Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
