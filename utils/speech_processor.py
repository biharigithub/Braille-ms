# ✅ Updated `utils/speech_processor.py`

from gtts import gTTS
import uuid
import os

AUDIO_DIR = os.path.join("static", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

def text_to_speech(text, language):
    try:
        lang_code = 'hi' if language.lower() == 'hindi' else 'en'
        tts = gTTS(text=text, lang=lang_code)
        
        filename = f"{uuid.uuid4().hex}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)
        
        tts.save(filepath)

        return f"/static/audio/{filename}"  # Return relative URL path
    except Exception as e:
        raise Exception(f"TTS failed: {str(e)}")
