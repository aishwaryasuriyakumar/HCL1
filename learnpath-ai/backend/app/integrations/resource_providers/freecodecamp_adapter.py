import logging
import httpx
from typing import List
from urllib.parse import quote
from app.integrations.resource_providers.base_provider import ResourceProvider
from app.schemas.resource import ResourceCandidate, AccessType, ProviderStatusItem

logger = logging.getLogger(__name__)

# Structured public freeCodeCamp curriculum index for fast offline fallback & high reliability
FCC_CURRICULUM_INDEX = [
    {
        "title": "Python for Beginners - Full Course",
        "url": "https://www.freecodecamp.org/news/python-for-beginners-full-course/",
        "skills": ["Python", "Programming Fundamentals"],
        "difficulty": "beginner",
        "resource_type": "interactive"
    },
    {
        "title": "Machine Learning with Python Certification",
        "url": "https://www.freecodecamp.org/learn/machine-learning-with-python/",
        "skills": ["Machine Learning", "Neural Networks", "TensorFlow", "Deep Learning"],
        "difficulty": "intermediate",
        "resource_type": "interactive"
    },
    {
        "title": "Vector Databases and Embeddings – A Beginner's Guide",
        "url": "https://www.freecodecamp.org/news/vector-databases-and-embeddings-guide/",
        "skills": ["Vector Databases", "Embeddings", "RAG"],
        "difficulty": "intermediate",
        "resource_type": "article"
    },
    {
        "title": "How to Build RAG Applications with Python and LangChain",
        "url": "https://www.freecodecamp.org/news/build-rag-apps-with-python-and-langchain/",
        "skills": ["RAG", "Prompt Engineering", "AI Agents", "Vector Databases"],
        "difficulty": "intermediate",
        "resource_type": "article"
    },
    {
        "title": "Fine-Tuning Large Language Models - A Practical Guide",
        "url": "https://www.freecodecamp.org/news/fine-tuning-llms-guide/",
        "skills": ["Fine-tuning", "Transformers", "LLM Evaluation"],
        "difficulty": "advanced",
        "resource_type": "article"
    },
    {
        "title": "Data Analysis with Python Certification",
        "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/",
        "skills": ["Data Science", "Pandas", "NumPy", "Data Visualization"],
        "difficulty": "beginner",
        "resource_type": "interactive"
    }
]

class FreeCodeCampAdapter(ResourceProvider):
    @property
    def platform_name(self) -> str:
        return "freeCodeCamp"

    def get_provider_status(self) -> ProviderStatusItem:
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
        candidates: List[ResourceCandidate] = []
        skills_lower = [s.lower() for s in skills]
        query_lower = query.lower()

        # Match against structured freeCodeCamp curriculum index
        for item in FCC_CURRICULUM_INDEX:
            match_score = 0
            for sk in item["skills"]:
                if any(sk_user in sk.lower() for sk_user in skills_lower):
                    match_score += 2
            if any(term in item["title"].lower() for term in query_lower.split()):
                match_score += 1

            if match_score > 0:
                candidates.append(
                    ResourceCandidate(
                        platform=self.platform_name,
                        title=item["title"],
                        original_url=item["url"],
                        description=f"Free interactive lesson/guide on {', '.join(item['skills'])}.",
                        resource_type=item.get("resource_type", "article"),
                        skills=item["skills"],
                        difficulty=item.get("difficulty", difficulty),
                        is_free=True,
                        access_type=AccessType.PUBLIC_FREE,
                        source_domain="freecodecamp.org",
                        is_active=True,
                        is_publicly_accessible=True,
                        metadata={"curriculum": "freeCodeCamp Public Index"}
                    )
                )

        # Fallback dynamic freeCodeCamp discovery via public news API/URL
        if len(candidates) < limit:
            primary_topic = skills[0] if skills else query
            dynamic_url = f"https://www.freecodecamp.org/news/search/?query={quote(primary_topic)}"
            candidates.append(
                ResourceCandidate(
                    platform=self.platform_name,
                    title=f"freeCodeCamp Guides & Tutorials: {primary_topic}",
                    original_url=dynamic_url,
                    description=f"Comprehensive free tutorials and code snippets covering {primary_topic}.",
                    resource_type="article",
                    skills=skills,
                    difficulty=difficulty,
                    is_free=True,
                    access_type=AccessType.PUBLIC_FREE,
                    source_domain="freecodecamp.org",
                    is_active=True,
                    is_publicly_accessible=True,
                    metadata={"search_topic": primary_topic}
                )
            )

        return candidates[:limit]
