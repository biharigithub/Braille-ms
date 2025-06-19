# utils/speech_processor.py

import os
import uuid
import asyncio
from edge_tts import Communicate

AUDIO_DIR = "static/audio"

def ensure_audio_dir():
    if not os.path.exists(AUDIO_DIR):
        os.makedirs(AUDIO_DIR)

def get_voice(language):
    return {
        'hindi': 'hi-IN-SwaraNeural',
        'english': 'en-US-AriaNeural'
    }.get(language, 'en-US-AriaNeural')

def text_to_speech(text, language='english'):
    ensure_audio_dir()
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)
    voice = get_voice(language)

    async def generate():
        communicate = Communicate(text=text, voice=voice)
        await communicate.save(filepath)

    asyncio.run(generate())
    return f"/static/audio/{filename}"
