import logging
import httpx
from datetime import datetime, timedelta
from typing import Tuple, Optional
from app.schemas.resource import ResourceCandidate, AccessType, VerificationStatus
from app.core.config import settings

logger = logging.getLogger(__name__)

class ResourceValidator:
    """
    Validates URL reachability, active status, and public accessibility safely via HTTP HEAD/GET.
    """

    def __init__(self, ttl_days: Optional[int] = None):
        self.ttl_days = ttl_days or settings.resource_verification_ttl_days

    def is_verification_fresh(self, last_verified_at: Optional[datetime]) -> bool:
        if not last_verified_at:
            return False
        cutoff = datetime.utcnow() - timedelta(days=self.ttl_days)
        return last_verified_at >= cutoff

    async def validate_candidate(
        self,
        candidate: ResourceCandidate,
        allow_paid: bool = False,
        allow_account_required: bool = True
    ) -> Tuple[ResourceCandidate, VerificationStatus]:
        """
        Validates URL reachability, active status, and public access compliance.
        Updates candidate attributes in-place and returns (candidate, status).
        """

        # 1. Access Type Filtering
        if candidate.access_type == AccessType.RESTRICTED:
            candidate.is_active = False
            candidate.is_publicly_accessible = False
            return candidate, VerificationStatus.RESTRICTED

        if candidate.access_type == AccessType.UNKNOWN:
            candidate.is_active = False
            candidate.is_publicly_accessible = False
            return candidate, VerificationStatus.ERROR

        if candidate.access_type == AccessType.PAID and not allow_paid:
            candidate.is_publicly_accessible = False
            return candidate, VerificationStatus.RESTRICTED

        if candidate.access_type == AccessType.PUBLIC_ACCOUNT_REQUIRED and not allow_account_required:
            candidate.is_publicly_accessible = False
            return candidate, VerificationStatus.RESTRICTED

        # 2. Re-use cached verification if fresh
        if self.is_verification_fresh(candidate.last_verified_at) and candidate.is_active:
            return candidate, VerificationStatus.VERIFIED

        # 3. HTTP Reachability Verification (HEAD -> fallback GET)
        headers = {
            "User-Agent": "LearnPath-AI-ResourceValidator/1.0 (Public Content Checker)"
        }

        url = candidate.original_url
        status_code = None

        try:
            async with httpx.AsyncClient(timeout=5.0, follow_redirects=True) as client:
                try:
                    resp = await client.head(url, headers=headers)
                    status_code = resp.status_code
                    if status_code in (405, 501):  # Method Not Allowed -> fallback GET
                        resp = await client.get(url, headers=headers)
                        status_code = resp.status_code
                except Exception:
                    # Fallback directly to GET if HEAD connection fails
                    resp = await client.get(url, headers=headers)
                    status_code = resp.status_code

        except httpx.HTTPStatusError as e:
            status_code = e.response.status_code
        except Exception as e:
            logger.debug(f"ResourceValidator reachability check failed for {url}: {e}")

        now = datetime.utcnow()
        candidate.last_verified_at = now

        if status_code and status_code in (200, 201, 204, 301, 302, 307, 308):
            candidate.is_active = True
            candidate.is_publicly_accessible = True
            return candidate, VerificationStatus.VERIFIED
        elif status_code in (404, 410):
            candidate.is_active = False
            candidate.is_publicly_accessible = False
            return candidate, VerificationStatus.INACTIVE
        elif status_code in (401, 403):
            candidate.is_active = True
            candidate.is_publicly_accessible = False
            return candidate, VerificationStatus.RESTRICTED
        else:
            # Handle rate limits (429), timeouts, or missing status code
            # Keep as unverified (soft fallback)
            candidate.is_active = True
            candidate.is_publicly_accessible = True
            return candidate, VerificationStatus.UNVERIFIED
