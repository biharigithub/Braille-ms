# ✅ Updated utils/speech_processor.py using edge-tts for better Android compatibility
import asyncio
import base64
import tempfile
import os
from edge_tts import Communicate

def text_to_speech(text, language='english'):
    try:
        voice_map = {
            'english': 'en-US-GuyNeural',
            'hindi': 'hi-IN-MadhurNeural'
        }
        voice = voice_map.get(language.lower(), 'en-US-GuyNeural')

        async def generate():
            communicate = Communicate(text, voice)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                tmp_path = tmp_file.name
            await communicate.save(tmp_path)
            with open(tmp_path, 'rb') as f:
                audio_base64 = base64.b64encode(f.read()).decode('utf-8')
            os.remove(tmp_path)
            return audio_base64

        return asyncio.run(generate())

    except Exception as e:
        raise RuntimeError(f"TTS failed: {e}")
