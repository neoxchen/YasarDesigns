from rate_limiter import RateLimiter
import secrets
import time

class Payload:
    def __init__(self, account_id):
        self.account_id = account_id

rate_limiter = RateLimiter()
payload1 = Payload("12345667")
payload2 = Payload("99999999")

payloads = [payload1, payload2]
endpoints = ["CreateItem"]


while True:
    response = rate_limiter.request(secrets.choice(endpoints), secrets.choice(payloads))
    print(response)
    time.sleep(1)
