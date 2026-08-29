import logging
from typing import List
from urllib.parse import quote
from app.integrations.resource_providers.base_provider import ResourceProvider
from app.schemas.resource import ResourceCandidate, AccessType, ProviderStatusItem

logger = logging.getLogger(__name__)

# Public MIT OpenCourseWare course index
MIT_OCW_INDEX = [
    {
        "title": "MIT 6.0001: Introduction to Computer Science and Programming in Python",
        "url": "https://ocw.mit.edu/courses/6-0001-introduction-to-computer-science-and-programming-in-python-fall-2016/",
        "skills": ["Python", "Programming Fundamentals", "Algorithms"],
        "difficulty": "beginner"
    },
    {
        "title": "MIT 6.036: Introduction to Machine Learning",
        "url": "https://ocw.mit.edu/courses/6-036-introduction-to-machine-learning-spring-2020/",
        "skills": ["Machine Learning", "Neural Networks", "Embeddings"],
        "difficulty": "intermediate"
    },
    {
        "title": "MIT 6.S191: Introduction to Deep Learning",
        "url": "https://ocw.mit.edu/courses/6-s191-introduction-to-deep-learning/",
        "skills": ["Deep Learning", "Transformers", "LLM Fundamentals", "Fine-tuning"],
        "difficulty": "intermediate"
    },
    {
        "title": "MIT 6.006: Introduction to Algorithms",
        "url": "https://ocw.mit.edu/courses/6-0006-introduction-to-algorithms-spring-2020/",
        "skills": ["Algorithms", "Data Structures", "Vector Databases"],
        "difficulty": "intermediate"
    }
]

class MITOpenCourseWareAdapter(ResourceProvider):
    @property
    def platform_name(self) -> str:
        return "MIT OpenCourseWare"

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

        # Match against structured MIT OCW course list
        for course in MIT_OCW_INDEX:
            match = False
            for sk in course["skills"]:
                if any(sk_user in sk.lower() for sk_user in skills_lower):
                    match = True
                    break

            if match:
                candidates.append(
                    ResourceCandidate(
                        platform=self.platform_name,
                        title=course["title"],
                        original_url=course["url"],
                        description=f"Full academic course materials from MIT covering {', '.join(course['skills'])}.",
                        resource_type="course",
                        skills=course["skills"],
                        difficulty=course.get("difficulty", difficulty),
                        is_free=True,
                        access_type=AccessType.PUBLIC_FREE,
                        source_domain="ocw.mit.edu",
                        is_active=True,
                        is_publicly_accessible=True,
                        metadata={"institution": "MIT OpenCourseWare"}
                    )
                )

        # Fallback search link
        if len(candidates) < limit:
            primary_topic = skills[0] if skills else query
            search_url = f"https://ocw.mit.edu/search/?q={quote(primary_topic)}"
            candidates.append(
                ResourceCandidate(
                    platform=self.platform_name,
                    title=f"MIT OpenCourseWare Search Results for {primary_topic}",
                    original_url=search_url,
                    description=f"Open courseware lecture notes, assignments, and exams for {primary_topic}.",
                    resource_type="course",
                    skills=skills,
                    difficulty=difficulty,
                    is_free=True,
                    access_type=AccessType.PUBLIC_FREE,
                    source_domain="ocw.mit.edu",
                    is_active=True,
                    is_publicly_accessible=True,
                    metadata={"search": True}
                )
            )

        return candidates[:limit]
