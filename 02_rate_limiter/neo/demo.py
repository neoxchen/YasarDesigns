"""
Requirements: Rate limiter for HTTP requests
1. Rate limit requests based on IP address? session ID?
2. Multiple rate limits for different APIs

Rate limit algorithm: "Token bucket"
- Tokens are added at a fixed rate
- Tokens are consumed when a request is made
- If there are no tokens, the request is rejected

Potential additional features:
1. "Panic mode" when the server is under heavy load, restrict X% of all requests
2. Maximum number of requests per minute across all APIs (server load)

"""
import time

from common import CacheAccess, MockedCacheAccess
from common import HttpRequest, HttpResponse
from rate_limit_decorator import rate_limit
from utilities import RateLimitRegistry

cache: CacheAccess = MockedCacheAccess()
registry: RateLimitRegistry = RateLimitRegistry("./rate_limits.yaml")


@rate_limit(registry, cache)
def default_api(request: HttpRequest) -> HttpResponse:
    return HttpResponse(200, {
        "message": "Request handled"
    })


@rate_limit(registry, cache)
def example_api_1(request: HttpRequest) -> HttpResponse:
    return HttpResponse(200, {
        "message": "Request handled"
    })


@rate_limit(registry, cache)
def example_api_2(request: HttpRequest) -> HttpResponse:
    return HttpResponse(200, {
        "message": "Request handled"
    })


if __name__ == "__main__":
    import uuid

    default_request: HttpRequest = HttpRequest("https://neoc.me", {
        "client_name": "default",
        "session_id": str(uuid.uuid4()),
    })
    custom_request: HttpRequest = HttpRequest("https://neoc.me", {
        "client_name": "custom_client",
        "session_id": str(uuid.uuid4()),
    })

    print(">" * 10)
    print(f"Starting demo:")

    count: int = 0
    while count < 5:
        print(f"\n>> Invocation #{count + 1} with default request")
        response: HttpResponse = default_api(default_request)
        print(f"<< Response: {response}")
        time.sleep(1)
        count += 1

    time.sleep(5)

    count: int = 0
    while count < 5:
        print(f"\n>> Invocation #{count + 1} with default request")
        response: HttpResponse = default_api(default_request)
        print(f"<< Response: {response}")
        time.sleep(1)
        count += 1
