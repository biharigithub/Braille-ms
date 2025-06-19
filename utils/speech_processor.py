from gtts import gTTS
import hashlib
import os
import base64
import tempfile

CACHE_DIR = "/tmp/tts_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def text_to_speech(text, language='english'):
    try:
        lang_code = 'hi' if language.lower() == 'hindi' else 'en'
        hash_key = hashlib.md5((text + lang_code).encode()).hexdigest()
        cached_file = os.path.join(CACHE_DIR, f"{hash_key}.mp3")

        if not os.path.exists(cached_file):
            tts = gTTS(text=text, lang=lang_code)
            tts.save(cached_file)

        with open(cached_file, "rb") as audio_file:
            audio_data = base64.b64encode(audio_file.read()).decode('utf-8')
        return audio_data

    except Exception as e:
        raise e
