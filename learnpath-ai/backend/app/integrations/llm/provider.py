import urllib.request
import json
import logging
from typing import Optional
from app.integrations.llm.base import BaseLLMProvider
from app.core.config import settings

logger = logging.getLogger(__name__)

class SimpleLLMProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = settings.llm_api_key
        # Default to gemini-1.5-flash if not specified
        self.model = settings.llm_model or "gemini-1.5-flash"

    def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        if not self.api_key:
            raise ValueError("LLM API Key is not configured.")

        # Construct official Gemini API endpoint url
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }
        
        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [
                    {"text": system_instruction}
                ]
            }

        headers = {
            "Content-Type": "application/json"
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                text = res_data["candidates"][0]["content"]["parts"][0]["text"]
                return text.strip()
        except Exception as e:
            logger.error(f"LLM API request failed: {e}")
            raise RuntimeError(f"Failed to generate text from LLM: {e}")

llm_provider = SimpleLLMProvider()
