# Point d’entrée global
import sys
import os

# Ajoute le dossier 'src' au chemin d'import
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SRC_PATH = os.path.join(BASE_DIR, "src")

sys.path.append(SRC_PATH)

VIDEO_INPUT_PATH = os.path.join(BASE_DIR, "data", "video_input.mp4")

from audio_processing.audio_extractor import extract_audio

from audio_processing.transcription import run_transcription


from dubbing.tts_kokoro_en import run_kokoro_pipeline


if __name__ == "__main__":
    print("EXTRACTING AUDIO...")
    
    extract_audio(VIDEO_INPUT_PATH)
    
    print("AUDIO EXTRACTION COMPLETE.")
    
    print("...")
    
    print("RUNNING TRANSCRIPTION...")
    
    run_transcription()
    
    print("TRANSCRIPTION COMPLETE.")

    print("...")
    
    print("RUNNING KOKORO PIPELINE...")
    
    run_kokoro_pipeline()

    print("KOKORO PIPELINE COMPLETE.")