# Extrait l’audio de la vidéo
import os
from moviepy.editor import VideoFileClip

# === PARAMÈTRES ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
VIDEO_INPUT = os.path.join(BASE_DIR, "data", "video_input.mp4")
OUTPUT_AUDIO_PATH = os.path.join(BASE_DIR, "data", "extracted_audio.wav")

def extract_audio(video_path=VIDEO_INPUT, output_audio_path=OUTPUT_AUDIO_PATH):
    """Extrait l’audio d’une vidéo et le sauvegarde en WAV."""
    print(f"xtraction audio depuis : {video_path}")
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(output_audio_path)
    print(f"Audio extrait vers : {output_audio_path}")
    return output_audio_path

# Pour exécution directe
if __name__ == "__main__":
    extract_audio()
