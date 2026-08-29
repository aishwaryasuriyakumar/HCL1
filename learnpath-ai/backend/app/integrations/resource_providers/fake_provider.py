from typing import List, Optional
from app.integrations.resource_providers.base_provider import ResourceProvider
from app.schemas.resource import ResourceCandidate, AccessType, ProviderStatusItem

class FakeResourceProvider(ResourceProvider):
    def __init__(
        self,
        platform_name: str = "FakeProvider",
        candidates: Optional[List[ResourceCandidate]] = None,
        is_available: bool = True
    ):
        self._platform_name = platform_name
        self.candidates = candidates or []
        self.is_available = is_available

    @property
    def platform_name(self) -> str:
        return self._platform_name

    def get_provider_status(self) -> ProviderStatusItem:
        if not self.is_available:
            return ProviderStatusItem(
                platform=self.platform_name,
                status="unavailable",
                reason="Simulated provider failure"
            )
        return ProviderStatusItem(
            platform=self.platform_name,
            status="available"
        )

    async def search(
        self,
        query: str,
        skills: List[str],
        difficulty: str = "intermediate",
        limit: int = 5
    ) -> List[ResourceCandidate]:
        if not self.is_available:
            return []

        if self.candidates:
            return self.candidates[:limit]

        # Generate default synthetic candidates with original URLs
        return [
            ResourceCandidate(
                platform=self.platform_name,
                title=f"Sample {self.platform_name} Video for {query}",
                original_url=f"https://example.com/{self.platform_name.lower()}/video1",
                description=f"Fake video tutorial covering {', '.join(skills)}.",
                resource_type="video",
                skills=skills,
                difficulty=difficulty,
                is_free=True,
                access_type=AccessType.PUBLIC_FREE,
                source_domain="example.com",
                is_active=True,
                is_publicly_accessible=True
            ),
            ResourceCandidate(
                platform=self.platform_name,
                title=f"Sample {self.platform_name} Article for {query}",
                original_url=f"https://example.com/{self.platform_name.lower()}/article1",
                description=f"Fake article covering {', '.join(skills)}.",
                resource_type="article",
                skills=skills,
                difficulty=difficulty,
                is_free=True,
                access_type=AccessType.PUBLIC_FREE,
                source_domain="example.com",
                is_active=True,
                is_publicly_accessible=True
            )
        ][:limit]
