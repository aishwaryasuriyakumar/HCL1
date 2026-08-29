import logging
import httpx
from typing import List, Optional
from datetime import datetime
from app.integrations.resource_providers.base_provider import ResourceProvider
from app.schemas.resource import ResourceCandidate, AccessType, ProviderStatusItem
from app.core.config import settings

logger = logging.getLogger(__name__)

class YouTubeAdapter(ResourceProvider):
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.youtube_api_key

    @property
    def platform_name(self) -> str:
        return "YouTube"

    def get_provider_status(self) -> ProviderStatusItem:
        if not self.api_key:
            return ProviderStatusItem(
                platform=self.platform_name,
                status="unavailable",
                reason="YOUTUBE_API_KEY not configured"
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
        if not self.api_key:
            logger.info("YouTubeAdapter: YOUTUBE_API_KEY not configured, skipping YouTube search.")
            return []

        search_query = f"{query} {' '.join(skills)} tutorial".strip()
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": search_query,
            "type": "video",
            "maxResults": limit,
            "key": self.api_key,
            "relevanceLanguage": "en",
            "safeSearch": "moderate"
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(url, params=params)
                if resp.status_code != 200:
                    logger.warning(f"YouTube API returned HTTP {resp.status_code}: {resp.text}")
                    return []

                data = resp.json()
                items = data.get("items", [])
                candidates = []

                for item in items:
                    id_info = item.get("id", {})
                    video_id = id_info.get("videoId")
                    if not video_id:
                        continue

                    snippet = item.get("snippet", {})
                    original_url = f"https://www.youtube.com/watch?v={video_id}"
                    title = snippet.get("title", "YouTube Video")
                    description = snippet.get("description", "")
                    published_at_str = snippet.get("publishedAt")
                    published_at = None
                    if published_at_str:
                        try:
                            published_at = datetime.fromisoformat(published_at_str.replace("Z", "+00:00"))
                        except Exception:
                            pass

                    candidate = ResourceCandidate(
                        platform=self.platform_name,
                        title=title,
                        original_url=original_url,
                        description=description,
                        resource_type="video",
                        skills=skills,
                        difficulty=difficulty,
                        is_free=True,
                        access_type=AccessType.PUBLIC_FREE,
                        published_at=published_at,
                        source_domain="youtube.com",
                        is_active=True,
                        is_publicly_accessible=True,
                        metadata={
                            "video_id": video_id,
                            "channel_title": snippet.get("channelTitle", ""),
                            "thumbnail_url": snippet.get("thumbnails", {}).get("default", {}).get("url", "")
                        }
                    )
                    candidates.append(candidate)

                return candidates

        except Exception as e:
            logger.error(f"YouTubeAdapter search failed: {e}")
            return []
