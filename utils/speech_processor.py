# utils/speech_processor.py
from gtts import gTTS
import base64
from io import BytesIO

def text_to_speech(text, language):
    try:
        lang_code = 'hi' if language.lower() == 'hindi' else 'en'
        tts = gTTS(text=text, lang=lang_code)
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        audio_data = base64.b64encode(fp.read()).decode('utf-8')
        return {'audio_data': audio_data}
    except Exception as e:
        return {'error': f"TTS failed: {str(e)}"}
