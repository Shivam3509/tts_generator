# 🎬 DocuGen AI: Beginner's Guide & Documentation

Welcome to **DocuGen AI**! This project is a powerful tool that helps you create documentary-style videos. It takes your text, turns it into a voice using AI, mixes it with background music, and then combines it with images to make a final video.

This guide is designed for beginners (freshers) to help you understand, set up, and run the project easily.

---

## 🌟 What does this project do?

The application is divided into two main steps:

1.  **Step 1: Audio Generation**

    - **Text-to-Speech**: Type or speak (using the microphone) your script.
    - **Voice Customization**: Choose different voices (English/Hindi) and adjust how fast or high-pitched they sound.
    - **Music Mixing**: Upload background music. The system automatically loops it and blends it with the voice.

2.  **Step 2: Video Production**
    - **Image Sequence**: Upload multiple images that tell your story.
    - **Auto-Sync**: The script you wrote in Step 1 is automatically carried over for subtitles.
    - **Final Export**: The system creates a professional MP4 video with transitions.

---

## 🛠️ Getting Started (Setup)

### 1. System Requirements

Before you start, you must have these two things on your computer:

- **Python**: Download and install the latest version from [python.org](https://www.python.org/).
- **FFmpeg**: This is a powerful "media engine" used for audio/video processing.
  - _Note_: Without FFmpeg, the project will **not** work. Make sure it's added to your system's "Environment Variables" (PATH).

### 2. Installing Libraries

Open your terminal (Command Prompt or PowerShell) and run this command to install the required Python packages:

```bash
pip install fastapi uvicorn edge-tts python-multipart aiohttp
```

---

## 🚀 How to Run the Project

1.  Open the project folder in your terminal.
2.  Start the server by running:
    ```bash
    python main.py
    ```
3.  You will see a message saying `Uvicorn running on http://0.0.0.0:8000`.
4.  Open your web browser (Chrome, Edge, etc.) and go to: `http://localhost:8000`

---

## 📂 Project Structure (Folder Map)

Understanding where files are located:

- 📂 **`static/`**: This contains the **Frontend** files.
  - `index.html`: The structure of the website.
  - `style.css`: The "Classic Monochrome" look (black & white theme).
- 📄 **`main.py`**: The **Brain** of the project. It handles requests from the website and communicates with the Python scripts.
- 📄 **`tts_generate.py`**: Handles everything related to **Audio** (Speech + Music Mixing).
- 📄 **`video_with_text.py`**: Handles everything related to **Video** (Images + Transitions).
- 📂 **`uploads/`**: This is where your uploaded images and music are temporarily stored.
- 📂 **`outputs/`**: This is where your finished audio and video files will appear.

---

## 💡 Pro Tips for Freshers

- **Microphone Usage**: When you use the Microphone (Voice-to-Text), speak clearly. It will detect if you selected a Hindi or English voice and transcribe accordingly.
- **FFmpeg Errors**: If you get an error saying "ffmpeg not found", it means you haven't installed FFmpeg or haven't added it to your system PATH.
- **Real-time Sync**: Notice that when you type in the Text-to-Speech box, it instantly appears in the Video Production box. This is called "Global State Sync" and it saves you time!

---

## 🎨 Theme Details

The app uses a **Classic Monochrome Theme**. We chose high-contrast Black & White to give it a "Cinematic Documentary" feel, making it look much more professional than standard colorful templates.

---

Happy Coding! If you have any issues, check the terminal for error logs.
