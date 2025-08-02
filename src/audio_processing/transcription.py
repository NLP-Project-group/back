import os
import whisper
import json

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

EXTRACTED_AUDIO_FILE = os.path.join(BASE_DIR, "data", "extracted_audio.wav")

# Chargement du modèle Whisper
model = whisper.load_model("medium")
print("Modèle chargé avec succès !")

# Transcrire de l'audio
assert os.path.isfile(EXTRACTED_AUDIO_FILE), f"Le fichier {EXTRACTED_AUDIO_FILE} est introuvable"
result = model.transcribe(EXTRACTED_AUDIO_FILE, verbose=True)

# Créer une liste de dictionnaires pour chaque segment
segments = []
for seg in result["segments"]:
    segment_info = {
        "start": round(seg["start"], 2),
        "end": round(seg["end"], 2),
        "text": seg["text"].strip()
    }
    print(f"Segment de {segment_info['start']} à {segment_info['end']}: {segment_info['text']}")
    segments.append(segment_info)

# Sauvegarder sous le fichier JSON 
output_path = os.path.join(BASE_DIR, "data", "segments.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(segments, f, ensure_ascii=False, indent=4)

print(f"✅ Transcription terminée et sauvegardée dans '{output_path}'")
