# utils/speech_processor.py
from gtts import gTTS
import os
from datetime import datetime

AUDIO_FOLDER = 'static/audio'
os.makedirs(AUDIO_FOLDER, exist_ok=True)

def text_to_speech(text, language):
    try:
        lang_code = 'hi' if language.lower() == 'hindi' else 'en'
        filename = f"tts_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.mp3"
        filepath = os.path.join(AUDIO_FOLDER, filename)
        tts = gTTS(text=text, lang=lang_code)
        tts.save(filepath)
        return {'audio_url': f'/static/audio/{filename}'}
    except Exception as e:
        return {'error': f"TTS failed: {str(e)}"}
