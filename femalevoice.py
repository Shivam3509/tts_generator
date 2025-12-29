import asyncio
import edge_tts
import os
import textwrap
import subprocess

# ===============================
# CONFIGURATION
# ===============================
VOICE = "hi-IN-SwaraNeural"  # Softer, more expressive female voice
RATE = "+0%"      # Normal pace for intimate storytelling
PITCH = "+2Hz"    # Slightly higher, warmer tone

AUDIO_OUTPUT = "Christmas_audio.mp3"
CHUNK_SIZE = 900  # safe for long text

# ===============================
# FULL SCRIPT
# ===============================
FULL_TEXT = """

"""

# ===============================
def split_text(text, chunk_size):
    return textwrap.wrap(text, chunk_size)

# ===============================
async def generate_audio():
    chunks = split_text(FULL_TEXT, CHUNK_SIZE)
    audio_files = []

    for i, chunk in enumerate(chunks):
        file_name = f"part_{i+1}.mp3"
        print(f"🔊 Generating audio: {file_name}")

        communicate = edge_tts.Communicate(
            text=chunk,
            voice=VOICE,
            rate=RATE,
            pitch=PITCH
        )

        await communicate.save(file_name)
        audio_files.append(file_name)

    # Merge all audio parts
    with open("audio_list.txt", "w", encoding="utf-8") as f:
        for file in audio_files:
            f.write(f"file '{file}'\n")

    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", "audio_list.txt",
        "-c", "copy",
        AUDIO_OUTPUT
    ], check=True)

    # Cleanup
    for f in audio_files:
        os.remove(f)
    os.remove("audio_list.txt")

    print(f"\n✅ FINAL AUDIO READY: {AUDIO_OUTPUT}")

# ===============================
if __name__ == "__main__":
    asyncio.run(generate_audio())