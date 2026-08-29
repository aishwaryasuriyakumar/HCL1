import logging
from typing import List, Optional
from urllib.parse import urlparse
from app.integrations.resource_providers.base_provider import ResourceProvider
from app.schemas.resource import ResourceCandidate, AccessType, ProviderStatusItem
from app.core.config import settings

logger = logging.getLogger(__name__)

# Structured database of official documentation pages for fast, reliable resolution
OFFICIAL_DOCS_INDEX = [
    {
        "domain": "docs.python.org",
        "title": "Python Official Documentation & Tutorials",
        "url": "https://docs.python.org/3/tutorial/",
        "skills": ["Python", "Programming Fundamentals"],
        "difficulty": "beginner"
    },
    {
        "domain": "huggingface.co",
        "title": "Hugging Face Documentation – Transformers & Datasets",
        "url": "https://huggingface.co/docs/transformers/index",
        "skills": ["Transformers", "Fine-tuning", "LLM Evaluation", "Embeddings"],
        "difficulty": "intermediate"
    },
    {
        "domain": "huggingface.co",
        "title": "Hugging Face Deep RL & AI Agents Course",
        "url": "https://huggingface.co/docs/agents/index",
        "skills": ["AI Agents", "Prompt Engineering"],
        "difficulty": "advanced"
    },
    {
        "domain": "developer.mozilla.org",
        "title": "MDN Web Docs – JavaScript & Web APIs",
        "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
        "skills": ["JavaScript", "Web Development"],
        "difficulty": "beginner"
    },
    {
        "domain": "pytorch.org",
        "title": "PyTorch Official Documentation & Tutorials",
        "url": "https://pytorch.org/tutorials/",
        "skills": ["PyTorch", "Deep Learning", "Neural Networks", "Fine-tuning"],
        "difficulty": "intermediate"
    },
    {
        "domain": "developers.google.com",
        "title": "Google Gemini API Official Documentation",
        "url": "https://developers.google.com/gemini-api/docs",
        "skills": ["Prompt Engineering", "LLM Fundamentals", "AI Agents", "Tokens & Context Windows"],
        "difficulty": "intermediate"
    },
    {
        "domain": "learn.microsoft.com",
        "title": "Microsoft Learn – Generative AI & Vector Search Documentation",
        "url": "https://learn.microsoft.com/en-us/azure/ai-services/",
        "skills": ["RAG", "Vector Databases", "Embeddings"],
        "difficulty": "intermediate"
    }
]

class DocumentationAdapter(ResourceProvider):
    def __init__(self, allowed_domains: Optional[List[str]] = None):
        self.allowed_domains = allowed_domains or settings.trusted_official_doc_domains

    @property
    def platform_name(self) -> str:
        return "Official Documentation"

    def get_provider_status(self) -> ProviderStatusItem:
        return ProviderStatusItem(
            platform=self.platform_name,
            status="available"
        )

    def is_domain_allowed(self, url: str) -> bool:
        try:
            domain = urlparse(url).netloc.lower()
            return any(domain == allowed.lower() or domain.endswith("." + allowed.lower()) for allowed in self.allowed_domains)
        except Exception:
            return False

    async def search(
        self,
        query: str,
        skills: List[str],
        difficulty: str = "intermediate",
        limit: int = 5
    ) -> List[ResourceCandidate]:
        candidates: List[ResourceCandidate] = []
        skills_lower = [s.lower() for s in skills]

        # Filter docs index matching allowed domains and skills
        for doc in OFFICIAL_DOCS_INDEX:
            if not self.is_domain_allowed(doc["url"]):
                continue

            match = False
            for sk in doc["skills"]:
                if any(sk_user in sk.lower() for sk_user in skills_lower):
                    match = True
                    break

            if match:
                candidates.append(
                    ResourceCandidate(
                        platform=self.platform_name,
                        title=doc["title"],
                        original_url=doc["url"],
                        description=f"Official technical documentation covering {', '.join(doc['skills'])}.",
                        resource_type="documentation",
                        skills=doc["skills"],
                        difficulty=doc.get("difficulty", difficulty),
                        is_free=True,
                        access_type=AccessType.PUBLIC_FREE,
                        source_domain=urlparse(doc["url"]).netloc,
                        is_active=True,
                        is_publicly_accessible=True,
                        metadata={"trusted_domain": True}
                    )
                )

        # Fallback for target skills to official documentation search page
        if len(candidates) < limit and skills:
            target_skill = skills[0]
            if "python" in target_skill.lower():
                fallback_url = "https://docs.python.org/3/"
            elif any(term in target_skill.lower() for term in ["transformer", "model", "fine-tuning", "rag", "eval"]):
                fallback_url = "https://huggingface.co/docs"
            else:
                fallback_url = "https://developer.mozilla.org"

            if self.is_domain_allowed(fallback_url):
                candidates.append(
                    ResourceCandidate(
                        platform=self.platform_name,
                        title=f"Official Reference Documentation: {target_skill}",
                        original_url=fallback_url,
                        description=f"Official reference guides and specs for {target_skill}.",
                        resource_type="documentation",
                        skills=skills,
                        difficulty=difficulty,
                        is_free=True,
                        access_type=AccessType.PUBLIC_FREE,
                        source_domain=urlparse(fallback_url).netloc,
                        is_active=True,
                        is_publicly_accessible=True,
                        metadata={"official_reference": True}
                    )
                )

        return candidates[:limit]
