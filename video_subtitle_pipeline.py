"""
🎬 Video Subtitle Pipeline
==========================
This script downloads a Chinese video (via m3u8 URL),
extracts its audio, performs speech recognition with Whisper,
and generates multilingual subtitles (Chinese → English → [Russian, French, Spanish, German]).

Author: Viacheslav Balagurov
License: MIT
"""

import os
import subprocess
import whisper
from tqdm import tqdm
import argostranslate.translate as argtr

# === USER SETTINGS ===

# Project base name (used for all output files)
PROJECT_NAME = "my_video"  # <- change this to your video name (no extension)

# Video source (m3u8 link or other)
M3U8_URL = "https://example.com/path/to/video/playlist.m3u8"

# Paths and tools
FFMPEG = "/opt/homebrew/bin/ffmpeg"  # path to FFmpeg binary
MODEL = "large-v3"                   # whisper models: tiny, base, small, medium, large, large-v2, large-v3

# Save options
SAVE_AUDIO = True
SAVE_ZH_SUB = True
SAVE_EN_SUB = True

# Choose which translated subtitle files to generate
SAVE_LANGS = {
    "ru": True,   # Russian
    "fr": False,  # French
    "es": False,  # Spanish
    "de": False,  # German
}

# === AUTO-GENERATED FILE NAMES ===
VIDEO_NAME = f"{PROJECT_NAME}.mp4"
AUDIO_NAME = f"{PROJECT_NAME}_audio.wav"
ZH_SUB = f"{PROJECT_NAME}_zh.srt"
EN_SUB = f"{PROJECT_NAME}_en.srt"
RU_SUB = f"{PROJECT_NAME}_ru.srt"
FR_SUB = f"{PROJECT_NAME}_fr.srt"
ES_SUB = f"{PROJECT_NAME}_es.srt"
DE_SUB = f"{PROJECT_NAME}_de.srt"


# === CORE FUNCTIONS ===

def timestamp(sec: float) -> str:
    """Convert seconds to SRT timestamp format."""
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    return f"{h:02}:{m:02}:{s:06.3f}".replace(".", ",")


def download_video():
    """Download the video if it does not already exist."""
    if os.path.exists(VIDEO_NAME):
        print("⏭️ Video already exists — skipping download.")
        return
    print("🎬 Downloading video...")
    subprocess.run(["yt-dlp", M3U8_URL, "-o", VIDEO_NAME, "--no-check-certificate"], check=True)
    print("✅ Video downloaded!\n")


def extract_audio():
    """Extract WAV audio track from the video."""
    if os.path.exists(AUDIO_NAME):
        print("⏭️ Audio already exists — skipping extraction.")
        return
    print("🎵 Extracting audio...")
    subprocess.run([FFMPEG, "-i", VIDEO_NAME, "-ac", "1", "-ar", "16000", "-vn", "-y", AUDIO_NAME], check=True)
    print("✅ Audio extracted!\n")


def recognize_and_translate_en():
    """Transcribe Chinese speech and translate it into English using Whisper."""
    print("🧠 Whisper is transcribing ZH → EN...")
    model = whisper.load_model(MODEL)
    result = model.transcribe(AUDIO_NAME, task="translate", language="zh")
    print("✅ Transcription complete!\n")
    return result["segments"]


def save_subtitles(segments, filename, text_key, lang_label):
    """Save SRT subtitles from Whisper segments."""
    print(f"📝 Saving {lang_label} subtitles...")
    with open(filename, "w", encoding="utf-8") as f:
        for i, seg in enumerate(segments, 1):
            f.write(f"{i}\n")
            f.write(f"{timestamp(seg['start'])} --> {timestamp(seg['end'])}\n")
            f.write(seg[text_key].strip() + "\n\n")
    print(f"✅ {lang_label} subtitles saved → {filename}\n")


def translate_and_save(segments, src_lang, dst_lang, filename, lang_label):
    """Translate subtitles from English to another language and save as SRT."""
    print(f"🌐 Translating {src_lang.upper()} → {dst_lang.upper()} ({lang_label})...")
    out_blocks = []
    for i, seg in enumerate(tqdm(segments, desc=f"Translating to {lang_label}")):
        en_text = seg["text"].strip()
        translated = argtr.translate(en_text, src_lang, dst_lang)
        out_blocks.append(f"{i+1}\n{timestamp(seg['start'])} --> {timestamp(seg['end'])}\n{translated}\n\n")
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(out_blocks)
    print(f"✅ {lang_label} subtitles saved → {filename}\n")


def main():
    """Main pipeline execution."""
    print(f"\n🎬 Starting subtitle pipeline for: {PROJECT_NAME}\n")

    download_video()

    if SAVE_AUDIO:
        extract_audio()
    else:
        print("⏭️ Audio extraction disabled.\n")

    # Step 1: Recognize Chinese → English
    segments = recognize_and_translate_en()

    # Step 2: Save Chinese subtitles (if enabled)
    if SAVE_ZH_SUB:
        print("🈶 Creating Chinese subtitles from original text (if available)...")
        with open(ZH_SUB, "w", encoding="utf-8") as f:
            for i, seg in enumerate(segments, 1):
                f.write(f"{i}\n")
                f.write(f"{timestamp(seg['start'])} --> {timestamp(seg['end'])}\n")
                zh_text = seg.get("original_text", seg.get("text", "")).strip()
                f.write(zh_text + "\n\n")
        print(f"✅ Chinese subtitles saved → {ZH_SUB}\n")
    else:
        print("⏭️ Skipping Chinese subtitles.\n")

    # Step 3: Save English subtitles (if enabled)
    if SAVE_EN_SUB:
        save_subtitles(segments, EN_SUB, "text", "English")
    else:
        print("⏭️ Skipping English subtitles.\n")

    # Step 4: Translate English → other languages (only enabled ones)
    lang_map = {
        "ru": ("Russian", RU_SUB),
        "fr": ("French", FR_SUB),
        "es": ("Spanish", ES_SUB),
        "de": ("German", DE_SUB)
    }

    for code, enabled in SAVE_LANGS.items():
        if not enabled:
            print(f"⏭️ Skipping translation to {code.upper()}.\n")
            continue
        lang_name, filename = lang_map[code]
        translate_and_save(segments, "en", code, filename, lang_name)

    # Step 5: Clean up audio file if saving is disabled
    if not SAVE_AUDIO and os.path.exists(AUDIO_NAME):
        os.remove(AUDIO_NAME)
        print("🗑️ Audio file removed (SAVE_AUDIO = False).")

    print(f"🎉 DONE! All subtitles for '{PROJECT_NAME}' created successfully.\n")


if __name__ == "__main__":
    main()