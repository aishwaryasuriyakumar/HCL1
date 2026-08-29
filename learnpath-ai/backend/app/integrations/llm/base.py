from abc import ABC, abstractmethod
from typing import Optional

class BaseLLMProvider(ABC):
    @abstractmethod
    def generate_text(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """
        Generate text based on a prompt and optional system instructions.
        """
        pass
