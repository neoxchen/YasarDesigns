import time
from typing import Any, Dict, Optional


############################################################################################################
# Interfaces
class RateLimitDefinition:
    def __init__(self, burst: int, rate: float):
        self.burst: int = burst
        self.rate: float = rate

    def __repr__(self):
        return f"RateLimitDefinition(burst={self.burst}, rate={self.rate})"


class ApiRateLimitDefinition:
    def __init__(self, default_limits: RateLimitDefinition, overrides: Dict[str, RateLimitDefinition]):
        self.default_limits: RateLimitDefinition = default_limits
        self.overrides: Dict[str, RateLimitDefinition] = overrides

    def get_rate_limit(self, actor_id: Optional[str] = None) -> RateLimitDefinition:
        if actor_id and actor_id in self.overrides:
            return self.overrides[actor_id]
        return self.default_limits

    @staticmethod
    def load(data: Dict[str, Any]) -> "ApiRateLimitDefinition":
        default_limits: RateLimitDefinition = RateLimitDefinition(data["default"]["burst"], data["default"]["rate"])
        override_limits: Dict[str, RateLimitDefinition] = {}
        for actor_id, limits in data.get("overrides", {}).items():
            override_limits[actor_id] = RateLimitDefinition(limits["burst"], limits["rate"])
        return ApiRateLimitDefinition(default_limits, override_limits)

    def __repr__(self):
        return f"ApiRateLimitDefinition(default_limits={self.default_limits}, overrides={self.overrides})"


class HttpRequest:
    def __init__(self, endpoint: str, payload: Dict[str, Any]):
        self.endpoint: str = endpoint
        self.payload: Dict[str, Any] = payload

    def __repr__(self):
        return f"HttpRequest(request_url={self.endpoint}, payload={self.payload})"


class HttpResponse:
    def __init__(self, status_code: int, payload: Dict[str, Any]):
        self.status_code: int = status_code
        self.payload: Dict[str, Any] = payload

    def __repr__(self):
        return f"HttpResponse(status_code={self.status_code}, payload={self.payload})"


############################################################################################################
# Database Layer -- likely Redis or some other in-memory database

class RateLimitEntry:
    def __init__(self, uuid: str, tokens: int, last_updated: int):
        self.uuid: str = uuid
        self.tokens: int = tokens
        self.last_updated: int = last_updated

    def __repr__(self):
        return f"RateLimitEntry(tokens={self.tokens}, last_updated={self.last_updated})"


class CacheAccess:
    def lookup(self, uuid: str) -> Optional[RateLimitEntry]:
        raise NotImplementedError

    def update(self, uuid: str, tokens: int) -> None:
        raise NotImplementedError

    def debug(self) -> None:
        raise NotImplementedError


class MockedCacheAccess(CacheAccess):
    def __init__(self):
        self.cache: Dict[str, RateLimitEntry] = {}

    def lookup(self, uuid: str) -> Optional[RateLimitEntry]:
        return self.cache.get(uuid)

    def update(self, uuid: str, tokens: int) -> None:
        timestamp = int(time.time())
        self.cache[uuid] = RateLimitEntry(uuid, tokens, timestamp)

    def debug(self) -> None:
        print(f"[DEBUG] Cache contents: {self.cache}")
