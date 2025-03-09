import base64
import hashlib
import secrets
import time
from typing import Optional

from interfaces import HttpResponse, DatabaseAccess, ShortUrlEntry
from interfaces import UrlShortener, UrlShortenerShortenRequest, UrlShortenerRedirectRequest

"""
Requirements:
- Shorten URLs
- Expiration time for short URLs
- # Custom name for short URLs, e.g. "s.neoc.me/As63Adle/wiggleyasar"
- X Per-user short URLs (i.e. 'unique' toggle), metrics, tracking, etc.

When shortening:
1. If [unique] is checked, regardless of the original URL, generate a new short URL
  - potentially using current timestamp? session ID?
2. If [custom name] is provided, store it
3. If [expiration time] is provided, add the expiration time to the short URL, otherwise -1 (infinite)

When redirecting:
1. If the short URL is found, redirect to the original URL if the expiration time has not passed
  - If a database entry is found but expired, wipe the entry and return a 404
  - If short url is found, regardless of custom name, redirect to the original URL
2. If the short URL is not found, return a 404

Periodic clean-up:
1. Short URLs that have expired should be removed from the database
2. Short URLs that does not have any clicks for [x] days should be removed from the database
"""

DEFAULT_URL_LENGTH: int = 6
MAX_URL_LENGTH: int = 15
BASE_URL_DOMAIN: str = "s.neoc.me"


def get_current_timestamp() -> int:
    return int(time.time())


class HashingUrlShortener(UrlShortener):
    def __init__(self, database: DatabaseAccess):
        self.database: DatabaseAccess = database

    def shorten(self, request: UrlShortenerShortenRequest) -> HttpResponse:
        # Generate a unique hash for the original URL
        salt: str = secrets.token_hex(16)
        url_hash: str = self.generate_hash(request.original_url, salt)
        timestamp: int = get_current_timestamp()

        # If the URL hash collides with the default length, increase the length
        url_length: int = DEFAULT_URL_LENGTH
        while True:
            print(f"[DEBUG] Attempting to shorten URL with length {url_length}: {url_hash[:url_length]}")
            if url_length > MAX_URL_LENGTH:
                return HttpResponse(500, {
                    "error": "Exceeded maximum URL length"
                })
            lookup_result: Optional[ShortUrlEntry] = self.database.lookup(url_hash[:url_length])
            if lookup_result is None or lookup_result.expiration_time > timestamp:
                break
            url_length += 1

        # Determine final URL and store in the database
        final_url: str = url_hash[:url_length]
        entry: ShortUrlEntry = ShortUrlEntry(request.original_url, final_url, timestamp + request.time_to_live)
        self.database.create(entry)

        return HttpResponse(200, {
            "short_url": f"https://{BASE_URL_DOMAIN}/{final_url}",
            "expiration_time": request.time_to_live,
        })

    def redirect(self, request: UrlShortenerRedirectRequest) -> HttpResponse:
        entry: Optional[ShortUrlEntry] = self.database.lookup(request.request_url)
        if entry is None:
            return HttpResponse(404, {
                "error": "Short URL not found"
            })

        # If the short URL has expired, delete the entry and return a 404
        if entry.expiration_time < get_current_timestamp():
            print(f"[DEBUG] Deleting expired short URL: {request.request_url}")
            self.database.delete(request.request_url)
            return HttpResponse(404, {
                "error": "Short URL not found"
            })

        # TODO: metrics, tracking, etc.

        # Redirect to the original URL
        return HttpResponse(301, {
            "original_url": entry.original_url
        })

    @staticmethod
    def generate_hash(url: str, salt: str = "") -> str:
        """ Generate a unique [a-zA-Z0-9] hash for the given URL, optionally with a salt """
        final_url: str = url + salt
        digest: str = hashlib.sha256(final_url.encode("utf-8")).hexdigest()
        b64_digest: bytes = base64.b64encode(digest.encode("utf-8"))
        decoded_b64_digest: str = b64_digest.decode("utf-8").replace("=", "")
        return decoded_b64_digest


if __name__ == "__main__":
    from typing import Dict, List


    class MockDatabase(DatabaseAccess):
        def __init__(self):
            self.database: dict[str, ShortUrlEntry] = {}

        def lookup(self, key: str) -> Optional[ShortUrlEntry]:
            return self.database.get(key)

        def create(self, entry: ShortUrlEntry) -> None:
            self.database[entry.short_url] = entry

        def delete(self, key: str) -> None:
            del self.database[key]


    database: DatabaseAccess = MockDatabase()
    url_shortener = HashingUrlShortener(database)

    urls_to_shorten: List[UrlShortenerShortenRequest] = [
        UrlShortenerShortenRequest("https://www.google.com", 1, "neoc", "google"),
        UrlShortenerShortenRequest("https://www.facebook.com", 2, "neoc", "facebook"),
        UrlShortenerShortenRequest("https://www.twitter.com", 3, "neoc", "twitter"),
        UrlShortenerShortenRequest("https://www.yasar.com", -1, "neoc", "yasar"),
    ]

    # Shorten the URL
    print(f"Shortening URLs:")
    url_map: Dict[str, str] = {}
    for request in urls_to_shorten:
        # print(f"Shortening URL: {original_url} with parameters: time_to_live={time_to_live}, actor_id={actor_id}, custom_name={custom_name}")
        print(f">> Shortening URL: {request.original_url} with parameters: time_to_live={request.time_to_live}, actor_id={request.actor_id}, custom_name={request.custom_name}")
        shorten_response: HttpResponse = url_shortener.shorten(request)
        print(f"<< Response: {shorten_response}")
        url_map[request.original_url] = shorten_response.payload["short_url"]

    # Redirect the URL within TTL
    time_elapsed: int = 0
    while time_elapsed < 5:
        time.sleep(1)

        for original_url, short_url in url_map.items():
            shortened_identifier: str = short_url.replace(f"https://{BASE_URL_DOMAIN}/", "")
            print(f"\nRedirecting URL within {time_elapsed} seconds: {short_url} ({shortened_identifier})")
            redirect_request: UrlShortenerRedirectRequest = UrlShortenerRedirectRequest(shortened_identifier)
            redirect_response: HttpResponse = url_shortener.redirect(redirect_request)
            print(redirect_response)

        time_elapsed += 1
