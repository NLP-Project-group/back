import json
import os
from transformers import pipeline
from langdetect import detect

# Construction des chemins de fichier
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
INPUT_FILE = os.path.join(BASE_DIR, "data", "segments.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "data", "translated_segments.json")


def detect_language(text):
    """Détecte la langue d’un texte"""
    try:
        detected = detect(text)
        return detected if detected in ['fr', 'en'] else 'en'
    except:
        french_words = ['le', 'la', 'les', 'de', 'du', 'et', 'est', 'dans', 'pour', 'avec']
        words = text.lower().split()[:5]
        return 'fr' if any(word in french_words for word in words) else 'en'


def load_translator(direction):
    """Charge un modèle de traduction selon la direction"""
    models = {
        "fr-en": "Helsinki-NLP/opus-mt-fr-en",
        "en-fr": "Helsinki-NLP/opus-mt-en-fr"
    }
    try:
        return pipeline("translation", model=models[direction])
    except Exception as e:
        print(f" Erreur chargement modèle {direction} : {e}")
        return None


def translate_text(text, translator):
    """Traduit un texte avec le traducteur donné"""
    try:
        result = translator(text)
        return result[0]["translation_text"]
    except Exception as e:
        print(f" Erreur de traduction : {e}")
        return text


def main():
    print(" Traduction des segments de texte")
    print("===================================")

    # Vérification du fichier d’entrée
    if not os.path.exists(INPUT_FILE):
        print(f" Fichier introuvable : {INPUT_FILE}")
        return

    # Lecture des segments
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            segments = json.load(f)
            if not isinstance(segments, list):
                raise ValueError("Le fichier doit contenir une liste de segments")
    except Exception as e:
        print(f" Erreur lecture fichier : {e}")
        return

    if not segments:
        print(" Aucun segment trouvé dans le fichier.")
        return

    print(f" {len(segments)} segments à traduire...")

    # Initialisation des traducteurs
    fr_to_en = None
    en_to_fr = None

    translated_segments = []

    # Traitement de chaque segment
    for i, segment in enumerate(segments):
        text = segment.get("text", "").strip()
        if not text:
            translated_segments.append({
                "start": segment.get("start"),
                "end": segment.get("end"),
                "original": "",
                "translation": ""
            })
            continue

        lang = detect_language(text)
        if lang == "fr":
            if fr_to_en is None:
                print(" Chargement modèle français → anglais...")
                fr_to_en = load_translator("fr-en")
            translator = fr_to_en
            direction = "🇫🇷→🇬🇧"
        else:
            if en_to_fr is None:
                print(" Chargement modèle anglais → français...")
                en_to_fr = load_translator("en-fr")
            translator = en_to_fr
            direction = "🇬🇧→🇫🇷"

        if translator is None:
            translation = text  # si échec, ne pas traduire
        else:
            translation = translate_text(text, translator)

        translated_segments.append({
            "start": segment.get("start"),
            "end": segment.get("end"),
            "text": translation
        })

        if i < 3 or (i + 1) % 10 == 0:
            print(f"{direction} [{i + 1}/{len(segments)}] {text[:30]}... → {translation[:30]}...")

    # Enregistrement du résultat
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(translated_segments, f, ensure_ascii=False, indent=2)
        print("\n Traduction terminée !")
        print(f" Résultat enregistré dans : {OUTPUT_FILE}")
        print(f" {len([seg for seg in translated_segments if seg['translation']])} traductions réussies")
    except Exception as e:
        pass


#if __name__ == "__main__":
 #   main()
