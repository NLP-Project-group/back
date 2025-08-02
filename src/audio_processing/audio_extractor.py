# Extrait l’audio de la vidéo
from moviepy import VideoFileClip


def extract_audio(video_path, output_audio_path="data/extracted_audio.wav"):
    video = VideoFileClip(video_path)
    audio = video.audio
    audio.write_audiofile(output_audio_path)
    
    return output_audio_path

if __name__ == "__main__":
    extract_audio("data/video_input.mp4")
