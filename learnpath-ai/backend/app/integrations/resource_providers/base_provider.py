from abc import ABC, abstractmethod
from typing import List
from app.schemas.resource import ResourceCandidate, ProviderStatusItem

class ResourceProvider(ABC):
    """
    Abstract base class for all public resource provider adapters.
    """

    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Returns the platform name (e.g. 'YouTube', 'freeCodeCamp', etc.)."""
        pass

    @abstractmethod
    async def search(
        self,
        query: str,
        skills: List[str],
        difficulty: str = "intermediate",
        limit: int = 5
    ) -> List[ResourceCandidate]:
        """
        Searches the provider for relevant learning resources and returns normalized ResourceCandidate objects.
        """
        pass

    @abstractmethod
    def get_provider_status(self) -> ProviderStatusItem:
        """
        Returns provider health and availability status.
        """
        pass
