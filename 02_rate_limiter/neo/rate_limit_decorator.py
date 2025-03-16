import time
from functools import wraps
from typing import Optional

from common import CacheAccess, RateLimitDefinition, RateLimitEntry
from common import HttpRequest, HttpResponse
from utilities import RateLimitRegistry


def generate_cache_key(function_name: str, client_name: str, session_id: str) -> str:
    return f"{function_name}:{client_name}:{session_id}"


def rate_limit(registry: RateLimitRegistry, cache: CacheAccess):
    def decorator(function: callable):
        @wraps(function)
        def wrapper(request: HttpRequest):
            client_name: str = request.payload.get("client_name", "default")
            session_id: str = request.payload.get("session_id", "default")
            print(f"[DEBUG] Processing rate limit for '{function.__name__}' with client '{client_name}' and session '{session_id}'")

            # Find the rate limit for the current request
            limit: RateLimitDefinition = registry.get_rate_limit(function.__name__, client_name)
            cache_key: str = generate_cache_key(function.__name__, client_name, session_id)
            current_limit: Optional[RateLimitEntry] = cache.lookup(cache_key)
            print(f"[DEBUG] Rate limit '{limit}' used '{current_limit}'")

            if not current_limit:
                current_limit = RateLimitEntry(cache_key, limit.burst, int(time.time()))

            # TODO: There is a bug in this replenishment logic and updating the cache logic
            # Calculate automatic token replenishment
            elapsed_time: int = int(time.time()) - current_limit.last_updated
            replenished_tokens: int = int(elapsed_time * limit.rate)

            # Calculate new token count
            new_tokens: int = min(max(current_limit.tokens + replenished_tokens, 0), limit.burst)
            print(f"[DEBUG] Replenished {replenished_tokens} tokens, new token count: {new_tokens}/{limit.burst}")

            # Check if rate limit is exceeded
            if new_tokens - 1 < 0:
                return HttpResponse(429, {
                    "message": "Rate limit exceeded"
                })

            # Update the cache with the new token count
            cache.update(cache_key, new_tokens - 1)

            # Call the function
            response: HttpResponse = function(request)
            return response

        return wrapper

    return decorator
