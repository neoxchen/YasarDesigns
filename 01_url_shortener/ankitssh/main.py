from url_converter_service import UrlService
from encoder_enum import Encoders
from database_enum import DataBases
url_service = UrlService(Encoders.HASH, DataBases.REDIS)

while(True):
    print("1. Shorten a URL ")
    print("2. Get Long URL Back")
    choice = int(input())
    match choice:
        case 1:
            print("Enter a long url")
            long_url = input()
            short_url = url_service.shorten_url(long_url)
            print(short_url)
        case 2: 
            print("Enter a short url")
            short_url = input()
            long_url = url_service.get_long_url(short_url)
            print(long_url)
    