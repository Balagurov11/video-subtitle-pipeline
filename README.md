🎬 Video Subtitle Pipeline

A simple Python tool for downloading Chinese videos, extracting audio, recognizing speech, and generating multilingual subtitles.
Supports translation pipeline: Chinese → English → [Russian, French, Spanish, German]

🚀 Features
	•	Download video via m3u8 (using yt-dlp)
	•	Extract audio via FFmpeg
	•	Transcribe Chinese → English using Whisper
	•	Translate English → multiple languages using Argos Translate
	•	Automatically generate .srt subtitles for all selected languages
	•	Enable or disable audio/subtitles saving via simple settings

🧰 Requirements
Before running, install dependencies:
pip install -r requirements.txt
Also make sure FFmpeg is installed on your system.

⚙️ Configuration
Edit the top of the script before running:

PROJECT_NAME = “my_video”  # Base name for all files
M3U8_URL = “https://example.com/path/to/video.m3u8”

SAVE_AUDIO = True
SAVE_ZH_SUB = True
SAVE_EN_SUB = True

SAVE_LANGS = {
 “ru”: True,   # Russian
 “fr”: False,  # French
 “es”: False,  # Spanish
 “de”: False   # German
}

If a language is set to False, its translation will not be performed — saving time and system resources.

🖥️ Usage
Run the script:
python video_subtitle_pipeline.py

Resulting files:
my_video.mp4
my_video_audio.wav
my_video_zh.srt
my_video_en.srt
my_video_ru.srt
my_video_fr.srt
my_video_es.srt
my_video_de.srt

📄 License
MIT — free to use, modify and share.


Описание на русском

Video Subtitle Pipeline — это Python-скрипт, который:
	1.	Скачивает китайское видео по ссылке (m3u8)
	2.	Извлекает аудио через FFmpeg
	3.	Распознаёт китайскую речь и переводит её на английский (Whisper)
	4.	Переводит английский текст на выбранные языки (Argos Translate)
	5.	Создаёт субтитры в формате .srt

Все настройки находятся в начале файла.
Если отключить язык, перевод на него выполняться не будет — это экономит время и ресурсы.


⭐ Author: Viacheslav Balagurov
📜 License: MIT
