import asyncio
import edge_tts
import os
import textwrap
import subprocess
import uuid
import shutil

# ===============================
# CONFIGURATION (Defaults)
# ===============================
DEFAULT_VOICE = "hi-IN-MadhurNeural"
DEFAULT_RATE = "+30%"
DEFAULT_PITCH = "-5Hz"
DEFAULT_AUDIO_OUTPUT = "power_audio.mp3"
CHUNK_SIZE = 900

# ===============================
# FULL SCRIPT
# ===============================
FULL_TEXT = """
अगर आज तुम्हें अचानक 10 करोड़ रुपये मिल जाएँ…
तो 5 साल बाद तुम अमीर रहोगे या फिर से वहीं, जहाँ आज हो?

सच कड़वा है —
पैसा किसी को अमीर नहीं बनाता…
सोच बनाती है।

और आज की कहानी…
तुम्हारी सोच बदल सकती है।

लोग अक्सर कहते हैं —
“गरीब इसलिए गरीब है क्योंकि उसके पास पैसा नहीं है।”

लेकिन सच्चाई ये है —
गरीब के पास सबसे ज़्यादा जो चीज़ होती है…
वो है गरीब सोच।

और अमीर के पास सबसे कीमती चीज़…
अमीर सोच।

पैसा बाद में आता है।

गरीब सोच कहती है —
“पहले पैसा आ जाए, फिर risk लेंगे।”

अमीर सोच कहती है —
“Risk लेंगे, तभी पैसा आएगा।”

गरीब सोच पूछती है —
“अगर fail हो गया तो?”

अमीर सोच पूछती है —
“अगर सीख गया तो?”

गरीब सोच हर महीने salary का इंतज़ार करती है।
अमीर सोच हर महीने skill, system और asset बनाती है।

गरीब सोच समय को बेचती है।
अमीर सोच समय को खरीदती है।

अब ध्यान से सुनो…

दो लोग हैं।
दोनों एक ही शहर में।
एक ही उम्र।
एक ही education।

फर्क सिर्फ सोच का।

पहला व्यक्ति सुबह उठते ही सोचता है —
“आज boss क्या बोलेगा?”
“Job जाएगी तो क्या होगा?”
“Salary इस बार भी कम पड़ जाएगी।”

डर से दिन शुरू होता है।
और डर में ही खत्म।

दूसरा व्यक्ति भी सुबह उठता है।
लेकिन उसके सवाल अलग हैं —

“आज मैं क्या सीख सकता हूँ?”
“आज कौन-सी skill improve करूँ?”
“आज कौन-सा system मेरे बिना भी पैसा कमा सकता है?”

वो नौकरी करता है…
लेकिन नौकरी उसकी पहचान नहीं होती।

गरीब सोच कहती है —
“पढ़ाई खत्म, सीखना खत्म।”

अमीर सोच कहती है —
“सीखना खत्म = growth खत्म।”

गरीब सोच free content ignore करती है।
अमीर सोच कहती है —
“Knowledge free है, ignorance महँगी।”

गरीब सोच status पर पैसा उड़ाती है —
महंगा phone, दिखावा, approval।

अमीर सोच investment पर पैसा लगाती है —
books, skills, network, business।

गरीब सोच लोगों से पूछती है —
“कितना कमा रहे हो?”

अमीर सोच पूछती है —
“कैसे कमा रहे हो?”

गरीब सोच short-term comfort चुनती है।
अमीर सोच long-term freedom।

अब एक लाइन याद रखो —

गरीब लोग पैसा देखकर खुश होते हैं।
अमीर लोग process देखकर।

गरीब सोच कहती है —
“इतना ही possible है।”

अमीर सोच कहती है —
“Limit सिर्फ दिमाग में है।”

गरीब सोच comparison में जलती है।
अमीर सोच inspiration में बदलती है।

गरीब सोच कहती है —
“वो lucky है।”

अमीर सोच कहती है —
“वो disciplined है।”

अब सच सुनने के लिए तैयार हो?

गरीब सोच हमेशा blame ढूंढती है —
system, government, boss, economy।

अमीर सोच responsibility लेती है —
“मेरी life मेरी ज़िम्मेदारी है।”

गरीब सोच comfort zone में मर जाती है।
अमीर सोच discomfort में grow करती है।

गरीब सोच कहती है —
“आज enjoy कर लेते हैं।”

अमीर सोच कहती है —
“आज sacrifice करेंगे ताकि कल choice हो।”

याद रखो —

अमीर बनने का मतलब luxury नहीं है।
अमीर बनने का मतलब choice है।

Choice —
काम करना या नहीं।
कहाँ रहना है।
किसके साथ रहना है।
किसके लिए जीना है।

और सबसे ज़रूरी बात —

गरीब सोच पैसे से डरती है।
अमीर सोच पैसे को tool मानती है।

अब सवाल ये नहीं है कि
तुम गरीब हो या अमीर।

सवाल ये है —

आज तुम किस तरह सोच रहे हो?

क्योंकि जिस दिन तुम्हारी सोच बदलेगी…
उस दिन पैसा अपने आप रास्ता ढूंढ लेगा।

और याद रखना —

तुम्हारी current situation तुम्हारी permanent destination नहीं है।
लेकिन तुम्हारी current सोच…
तुम्हारा future तय कर सकती है।

अगर आज एक ही चीज़ बदलनी हो —
तो पैसा नहीं…
सोच बदलो।

क्योंकि…

अमीर पहले सोचते हैं।
फिर बनते हैं।

“पैसा दिमाग से आता है…
और दिमाग बदलने में
सिर्फ एक decision लगता है।”
"""

# ===============================
def split_text(text, chunk_size):
    return textwrap.wrap(text, chunk_size)

# ===============================
# ===============================
async def generate_audio(text, voice=DEFAULT_VOICE, rate=DEFAULT_RATE, pitch=DEFAULT_PITCH, output_path=DEFAULT_AUDIO_OUTPUT, bg_music_path=None, bg_volume=0.2):
    job_id = uuid.uuid4().hex
    chunks = split_text(text, CHUNK_SIZE)
    audio_files = []

    for i, chunk in enumerate(chunks):
        file_name = f"part_{i+1}_{job_id}.mp3"
        print(f"Generating audio: {file_name}")

        communicate = edge_tts.Communicate(
            text=chunk,
            voice=voice,
            rate=rate,
            pitch=pitch
        )

        await communicate.save(file_name)
        audio_files.append(file_name)

    # Merge all audio parts
    list_file = f"audio_list_{job_id}.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for file in audio_files:
            f.write(f"file '{file}'\n")

    temp_voice_file = None
    try:
        full_bg_path = os.path.abspath(bg_music_path) if bg_music_path else None
        full_output_path = os.path.abspath(output_path)
        
        # Step 1: Concatenate voice parts into a temporary file
        temp_voice_file = f"temp_voice_{job_id}.mp3"
        print(f"DEBUG: Concatenating voice parts into {temp_voice_file}")
        
        concat_cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", list_file,
            "-c", "copy",
            temp_voice_file
        ]
        result = subprocess.run(concat_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"DEBUG: FFMPEG ERROR (Concat):\n{result.stderr}")
            raise Exception(f"FFmpeg concat failed: {result.stderr}")
        else:
            print("DEBUG: FFmpeg Concat successful.")
        
        # Step 2: Mix with background music if provided
        if full_bg_path and os.path.exists(full_bg_path):
            bg_size = os.path.getsize(full_bg_path)
            print(f"DEBUG: Mixing voice with BG music. Path: {full_bg_path}, Size: {bg_size} bytes, Volume: {bg_volume}")
            
            # Get duration of voice audio
            duration_cmd = [
                "ffprobe", "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                temp_voice_file
            ]
            duration_result = subprocess.run(duration_cmd, capture_output=True, text=True)
            voice_duration = float(duration_result.stdout.strip()) if duration_result.returncode == 0 else 0
            print(f"DEBUG: Voice duration: {voice_duration} seconds")
            
            # Mix voice with looping background music
            # The background will loop and be trimmed to match voice duration
            mix_cmd = [
                "ffmpeg", "-y",
                "-i", temp_voice_file,
                "-stream_loop", "-1",
                "-i", full_bg_path,
                "-filter_complex",
                f"[0:a]volume=1.0[voice];[1:a]volume={bg_volume},aloop=loop=-1:size=2e+09[bg];[voice][bg]amix=inputs=2:duration=first[out]",
                "-map", "[out]",
                "-ac", "2",
                "-ar", "44100",
                "-t", str(voice_duration) if voice_duration > 0 else "999999",
                full_output_path
            ]
            print(f"DEBUG: Running mix command: {' '.join(mix_cmd)}")
            result = subprocess.run(mix_cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"DEBUG: FFMPEG ERROR (Mix):\n{result.stderr}")
                raise Exception(f"FFmpeg mix failed: {result.stderr}")
            else:
                print("DEBUG: FFmpeg Mix successful.")
        else:
            print(f"DEBUG: No BG music. Moving temp voice to output. BG Path provided: {bg_music_path}")
            # No background music, just move the concatenated voice file
            if os.path.exists(temp_voice_file):
                shutil.move(temp_voice_file, full_output_path)
                temp_voice_file = None  # Prevent deletion in finally block
            
    except Exception as e:
        print(f"Error in generate_audio: {e}")
        raise
    finally:
        # Cleanup
        for f in audio_files:
            if os.path.exists(f):
                os.remove(f)
        if os.path.exists(list_file):
            os.remove(list_file)
        if temp_voice_file and os.path.exists(temp_voice_file):
            os.remove(temp_voice_file)

    print(f"FINAL AUDIO READY: {output_path}")
    return output_path

# ===============================
if __name__ == "__main__":
    import textwrap
    FULL_TEXT = """
अगर आज तुम्हें अचानक 10 करोड़ रुपये मिल जाएँ…
तो 5 साल बाद तुम अमीर रहोगे या फिर से वहीं, जहाँ आज हो?
... (rest of the text)
"""
    asyncio.run(generate_audio(FULL_TEXT))
