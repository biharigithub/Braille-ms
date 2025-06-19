# utils/speech_processor.py

import pyttsx3
import os
import uuid

AUDIO_DIR = os.path.join("static", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

def text_to_speech(text, language='english'):
    engine = pyttsx3.init()

    # Set language voice
    voices = engine.getProperty('voices')
    if language == 'hindi':
        # Try to set Hindi voice (you must install Hindi voice in OS)
        for voice in voices:
            if 'hi' in voice.languages or 'Hindi' in voice.name:
                engine.setProperty('voice', voice.id)
                break
    else:
        # Use default English voice
        engine.setProperty('voice', voices[0].id)

    # Generate unique filename
    filename = f"tts_{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)

    engine.save_to_file(text, filepath)
    engine.runAndWait()

    return f"/static/audio/{filename}"
