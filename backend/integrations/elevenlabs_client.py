"""ElevenLabs Text-to-Speech client"""
from elevenlabs.client import ElevenLabs
from elevenlabs import save
import os
import hashlib
import structlog

from backend.config import settings
from backend.cache import cache

logger = structlog.get_logger()


class ElevenLabsClient:
    """ElevenLabs TTS client"""
    
    def __init__(self):
        self.client = ElevenLabs(api_key=settings.ELEVENLABS_API_KEY)
        self.default_voice_id = settings.ELEVENLABS_VOICE_ID
        self.model = settings.ELEVENLABS_MODEL
        self.audio_cache_dir = "backend/static/audio_cache"
        os.makedirs(self.audio_cache_dir, exist_ok=True)
    
    async def text_to_speech(
        self,
        text: str,
        user_id: int,
        voice_id: str = None
    ) -> str:
        """Convert text to speech and return audio URL"""
        voice_id = voice_id or self.default_voice_id
        
        # Check cache first
        cache_key = self._get_cache_key(text, voice_id)
        cached_url = await cache.get(f"audio:{cache_key}")
        
        if cached_url:
            logger.debug("Audio cache hit", text=text[:30])
            return cached_url
        
        try:
            # Generate audio
            audio = self.client.generate(
                text=text,
                voice=voice_id,
                model=self.model
            )
            
            # Save to file
            filename = f"{cache_key}.mp3"
            filepath = os.path.join(self.audio_cache_dir, filename)
            save(audio, filepath)
            
            # Generate URL
            audio_url = f"/static/audio_cache/{filename}"
            
            # Cache URL
            await cache.set(f"audio:{cache_key}", audio_url, ttl=86400)  # 24 hours
            
            logger.info("Audio generated", text=text[:30], voice_id=voice_id)
            return audio_url
            
        except Exception as e:
            logger.error("TTS generation failed", error=str(e))
            return ""

    
    def _get_cache_key(self, text: str, voice_id: str) -> str:
        """Generate cache key for audio"""
        content = f"{text}:{voice_id}"
        return hashlib.md5(content.encode()).hexdigest()
    
    async def get_available_voices(self):
        """Get list of available voices"""
        try:
            voices = self.client.voices.get_all()
            return [{"id": v.voice_id, "name": v.name} for v in voices.voices]
        except Exception as e:
            logger.error("Failed to get voices", error=str(e))
            return []


elevenlabs_client = ElevenLabsClient()
