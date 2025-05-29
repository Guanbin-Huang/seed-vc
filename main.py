import os
import subprocess
from client_seed_vc import batch_voice_convert
import sys

SRC_VID_DIR = "./src_vid"
EXTRACTED_AUDIO_DIR = "./extracted_audio"
OUTPUT_AUDIO_DIR = "./output_audio"
OUTPUT_VID_DIR = "./output_vid"
TARGET_AUDIO = "lzl.MP3"

os.makedirs(EXTRACTED_AUDIO_DIR, exist_ok=True)
os.makedirs(OUTPUT_AUDIO_DIR, exist_ok=True)
os.makedirs(OUTPUT_VID_DIR, exist_ok=True)

# 1. 提取音频
def has_audio_stream(video_path):
    result = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "a",
            "-show_entries", "stream=codec_type", "-of", "default=nw=1",
            video_path
        ],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    return b"codec_type=audio" in result.stdout

for filename in os.listdir(SRC_VID_DIR):
    if filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
        video_path = os.path.join(SRC_VID_DIR, filename)
        if not has_audio_stream(video_path):
            print(f"跳过无音频流的视频: {filename}")
            continue
        audio_path = os.path.join(EXTRACTED_AUDIO_DIR, os.path.splitext(filename)[0] + ".mp3")
        subprocess.run([
            "ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "libmp3lame", audio_path
        ], check=True)

# 2. 声音转换
try:
    batch_voice_convert(
        source_dir=EXTRACTED_AUDIO_DIR,
        output_dir=OUTPUT_AUDIO_DIR,
        target_audio=TARGET_AUDIO
    )
except Exception as e:
    print(f"[FATAL] batch_voice_convert failed: {e}")
    sys.exit(1)

# 3. 合成新视频
for filename in os.listdir(SRC_VID_DIR):
    if filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
        video_path = os.path.join(SRC_VID_DIR, filename)
        audio_path = os.path.join(OUTPUT_AUDIO_DIR, os.path.splitext(filename)[0] + "_result.wav")
        output_path = os.path.join(OUTPUT_VID_DIR, filename)
        if os.path.exists(audio_path):
            subprocess.run([
                "ffmpeg", "-y", "-i", video_path, "-i", audio_path, "-c:v", "copy", "-map", "0:v:0", "-map", "1:a:0", "-shortest", output_path
            ], check=True) 