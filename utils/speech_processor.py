# utils/speech_processor.py
from gtts import gTTS
import os
import uuid

AUDIO_FOLDER = 'static/audio'

# Ensure audio folder exists
os.makedirs(AUDIO_FOLDER, exist_ok=True)

def text_to_speech(text, language):
    try:
        lang_code = 'hi' if language.lower() == 'hindi' else 'en'
        tts = gTTS(text=text, lang=lang_code)

        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(AUDIO_FOLDER, filename)

        tts.save(filepath)

        # Return the URL path for frontend use
        return f"/static/audio/{filename}"
    except Exception as e:
        raise Exception(f"TTS failed: {str(e)}")
