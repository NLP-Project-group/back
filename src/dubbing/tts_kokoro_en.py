import os
import json
import soundfile as sf
from kokoro import KPipeline
from pydub import AudioSegment

# === PARAMÈTRES GÉNÉRAUX ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INPUT_JSON = os.path.join(BASE_DIR, "data", "translated_segments.json")
OUTPUT_AUDIO_DIR = os.path.join(BASE_DIR, "data", "output", "audio_output")
OUTPUT_AUDIO_TIMED = os.path.join(BASE_DIR, "data", "output", "dubbed_timed_audio.wav")
FINAL_VIDEO = os.path.join(BASE_DIR, "data", "output", "video_output", "final_dubbed_video.mp4")
VIDEO_INPUT = os.path.join(BASE_DIR, "data", "video_input.mp4")

os.makedirs(OUTPUT_AUDIO_DIR, exist_ok=True)
os.makedirs(os.path.dirname(FINAL_VIDEO), exist_ok=True)

def generate_tts_segments():
    """Génère les segments audio TTS et retourne le mapping des timecodes."""
    pipeline = KPipeline(lang_code='f')
    segment_map = []
    max_end = 0

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        segments = json.load(f)

    for i, seg in enumerate(segments):
        text = seg["text"]
        start = seg["start"]
        end = seg["end"]
        duration = end - start

        generator = pipeline(text, voice='af_sarah', speed=1.0)

        for j, (gs, ps, audio) in enumerate(generator):
            filename = f"segment_{i:03d}.wav"
            filepath = os.path.join(OUTPUT_AUDIO_DIR, filename)
            sf.write(filepath, audio, 24000)
            segment_map.append((start, filepath))
            max_end = max(max_end, end)

    return segment_map, max_end

def assemble_audio_track(segment_map, max_end):
    """Assemble les segments audio dans une piste synchronisée."""
    total_duration_ms = int(max_end * 1000)
    final_audio = AudioSegment.silent(duration=total_duration_ms, frame_rate=24000)

    for start_sec, filepath in segment_map:
        segment_audio = AudioSegment.from_wav(filepath)
        insert_pos = int(start_sec * 1000)
        final_audio = final_audio.overlay(segment_audio, position=insert_pos)

    final_audio.export(OUTPUT_AUDIO_TIMED, format="wav")
    print(f"Audio synchronisé exporté : {OUTPUT_AUDIO_TIMED}")

def replace_audio_in_video():
    """Remplace l’audio original de la vidéo par l’audio TTS synchronisé."""
    ffmpeg_cmd = f'ffmpeg -y -i "{VIDEO_INPUT}" -i "{OUTPUT_AUDIO_TIMED}" -c:v copy -map 0:v:0 -map 1:a:0 -shortest "{FINAL_VIDEO}"'
    os.system(ffmpeg_cmd)
    print(f"Vidéo finale enregistrée : {FINAL_VIDEO}")

def cleanup_temp_files():
    """Supprime les fichiers audio temporaires."""
    for file in os.listdir(OUTPUT_AUDIO_DIR):
        if file.endswith(".wav"):
            os.remove(os.path.join(OUTPUT_AUDIO_DIR, file))

    if os.path.exists(OUTPUT_AUDIO_TIMED):
        os.remove(OUTPUT_AUDIO_TIMED)

    print("Fichiers audio temporaires supprimés.")

def run_kokoro_pipeline():
    """Pipeline complet TTS + synchronisation + export vidéo."""
    print("Lancement du pipeline Kokoro TTS...")
    segment_map, max_end = generate_tts_segments()
    assemble_audio_track(segment_map, max_end)
    replace_audio_in_video()
    cleanup_temp_files()
    print("Pipeline terminé.")

# Pour exécution directe
if __name__ == "__main__":
    run_kokoro_pipeline()
