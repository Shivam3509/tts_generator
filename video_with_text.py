import subprocess
import os
import glob

# ===============================
# CONFIG (Defaults)
# ===============================
DEFAULT_IMAGES_FOLDER = "new_year"
DEFAULT_VOICE_AUDIO = "power_audio.mp3"
DEFAULT_OUTPUT_VIDEO = "final_video.mp4"

# Video dimensions
VIDEO_FORMATS = {
    "16:9": {"width": 1920, "height": 1080},  # YouTube Long Video
    "9:16": {"width": 1080, "height": 1920}   # YouTube Shorts
}

TRANSITION_DURATION = 1.0
TRANSITION_TYPE = "fade"

# ===============================
# AUDIO DURATION
# ===============================
def get_audio_duration(audio_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_path
    ]
    return float(subprocess.run(cmd, capture_output=True, text=True).stdout.strip())

# ===============================
# LOAD IMAGES
# ===============================
def get_images(folder):
    images = []
    for ext in ("*.png", "*.jpg", "*.jpeg", "*.PNG", "*.JPG", "*.JPEG"):
        images.extend(glob.glob(os.path.join(folder, ext)))

    if not images:
        raise RuntimeError(f"No images found in {folder}")

    print(f"Before sorting - found {len(images)} images:")
    for img in images:
        print(f"  {os.path.basename(img)}")

    # Sort in ascending order by number (11, 12, 13...)
    def extract_number(name):
        import re
        basename = os.path.basename(name)
        nums = re.findall(r"\d+", basename)
        num = int(nums[0]) if nums else 9999
        print(f"    Extracted {num} from {basename}")
        return num

    images.sort(key=extract_number)
    
    # Debug: print final sorted order
    print(f"\nAfter sorting - images in order:")
    for idx, img in enumerate(images):
        print(f"  Position {idx+1}: {os.path.basename(img)}")
    
    return images

# ===============================
# IMAGE DURATIONS (SCRIPT-AWARE)
# ===============================
def get_image_durations(audio_duration, count):
    base = audio_duration / count
    durations = []
    for i in range(count):
        factor = 0.8 if i % 2 == 0 else 1.2
        durations.append(round(base * factor, 2))
    return durations

# ===============================
# VIDEO CREATION (SIMPLIFIED)
# ===============================
def create_video(audio_duration, images, voice_audio, output_video, video_format="9:16"):
    # Get video dimensions based on format
    dimensions = VIDEO_FORMATS.get(video_format, VIDEO_FORMATS["9:16"])
    video_width = dimensions["width"]
    video_height = dimensions["height"]
    
    count = len(images)
    durations = get_image_durations(audio_duration, count)

    filter_parts = []
    zoom_speeds = [0.0006, 0.0008, 0.001]

    # Prepare images (Ken Burns + pixel format)
    for i in range(count):
        speed = zoom_speeds[i % len(zoom_speeds)]
        filter_parts.append(
            f"[{i}:v]"
            f"scale={video_width}:{video_height}:force_original_aspect_ratio=decrease,"
            f"pad={video_width}:{video_height}:(ow-iw)/2:(oh-ih)/2:black,"
            f"zoompan=z='min(zoom+{speed},1.08)':"
            f"d=1:s={video_width}x{video_height}:fps=30,"
            f"format=yuv420p,setsar=1[v{i}]"
        )

    # First transition
    filter_parts.append(
        f"[v0][v1]xfade=transition={TRANSITION_TYPE}:"
        f"duration={TRANSITION_DURATION}:"
        f"offset={durations[0] - TRANSITION_DURATION}[vf0]"
    )

    # Remaining transitions
    current_time = durations[0]
    for i in range(2, count):
        filter_parts.append(
            f"[vf{i-2}][v{i}]xfade=transition={TRANSITION_TYPE}:"
            f"duration={TRANSITION_DURATION}:"
            f"offset={current_time}[vf{i-1}]"
        )
        current_time += durations[i-1]

    video_stream = f"[vf{count-2}]"

    filter_complex = ";".join(filter_parts)

    # Inputs
    inputs = []
    for img in images:
        inputs.extend(["-loop", "1", "-i", img])

    inputs.extend(["-i", voice_audio])

    subprocess.run([
        "ffmpeg", "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", video_stream,
        "-map", f"{count}:a",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        "-t", str(audio_duration),
        output_video
    ], check=True)

def create_full_video(images_folder, voice_audio, output_video, video_format="9:16"):
    print(f"Starting video creation... Format: {video_format}")
    images = get_images(images_folder)
    duration = get_audio_duration(voice_audio)
    print(f"Audio duration: {duration:.2f}s")
    create_video(duration, images, voice_audio, output_video, video_format)
    print("FINAL VIDEO CREATED:", output_video)
    return output_video

# ===============================
if __name__ == "__main__":
    create_full_video(DEFAULT_IMAGES_FOLDER, DEFAULT_VOICE_AUDIO, DEFAULT_OUTPUT_VIDEO, "9:16")
