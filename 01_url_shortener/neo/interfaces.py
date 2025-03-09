from typing import Any, Dict, Optional


############################################################################################################
# Interfaces
class UrlShortenerShortenRequest:
    def __init__(self, original_url: str, time_to_live: int = -1, actor_id: Optional[str] = None, custom_name: Optional[str] = None):
        self.original_url: str = original_url
        self.time_to_live: int = time_to_live

        self.actor_id: Optional[str] = actor_id
        self.custom_name: Optional[str] = custom_name


class UrlShortenerRedirectRequest:
    def __init__(self, request_url: str):
        self.request_url: str = request_url


class HttpResponse:
    def __init__(self, status_code: int, payload: Dict[str, Any]):
        self.status_code: int = status_code
        self.payload: Dict[str, Any] = payload

    def __repr__(self):
        return f"HttpResponse(status_code={self.status_code}, payload={self.payload})"


class UrlShortener:
    def shorten(self, request: UrlShortenerShortenRequest) -> HttpResponse:
        raise NotImplementedError

    def redirect(self, request: UrlShortenerRedirectRequest) -> HttpResponse:
        raise NotImplementedError


############################################################################################################
# Database Layer
class DatabaseAccess:
    def lookup(self, key: str) -> Optional["ShortUrlEntry"]:
        raise NotImplementedError

    def create(self, entry: "ShortUrlEntry") -> None:
        raise NotImplementedError

    def delete(self, key: str) -> None:
        raise NotImplementedError


class ShortUrlEntry:
    """ Short URL entry in the database """

    def __init__(self, original_url: str, short_url: str, expiration_time: int = -1):
        self.original_url: str = original_url
        self.short_url: str = short_url
        self.expiration_time: int = expiration_time

    @staticmethod
    def load(short_url: str, database: DatabaseAccess) -> Optional["ShortUrlEntry"]:
        pass

    def save(self, database: DatabaseAccess):
        pass


############################################################################################################
# Metrics Layer
class MetricsAccess:
    def record_click(self, short_url: str, timestamp: int):
        raise NotImplementedError

    def cleanup(self):
        raise NotImplementedError
