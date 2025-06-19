import os
from gtts import gTTS
from datetime import datetime

AUDIO_FOLDER = 'static/audio'
os.makedirs(AUDIO_FOLDER, exist_ok=True)

def text_to_speech(text, language='english'):
    try:
        lang_code = 'hi' if language.lower() == 'hindi' else 'en'
        filename = f'tts_{datetime.now().strftime("%Y%m%d%H%M%S%f")}.mp3'
        filepath = os.path.join(AUDIO_FOLDER, filename)

        tts = gTTS(text=text, lang=lang_code)
        tts.save(filepath)

        return f'/static/audio/{filename}'
    except Exception as e:
        raise RuntimeError(f"TTS generation failed: {str(e)}")
