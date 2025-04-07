import base64
import hashlib
import hmac
import time
from typing import Optional, Dict


class TimeBasedOTPGenerator:
    def __init__(self, secret: str, time_step: int = 30):
        self.secret: bytes = base64.b32decode(secret, casefold=True)
        self.time_step: int = time_step

    def generate_otp(self, for_time: Optional[int] = None) -> str:
        if for_time is None:
            for_time = int(time.time())
        return self.compute_otp(for_time // 30)

    def compute_otp(self, time_period: int) -> str:
        hasher: hmac.HMAC = hmac.new(self.secret, self.int_to_bytestring(time_period), hashlib.sha1)
        hmac_hash: bytearray = bytearray(hasher.digest())
        offset: int = hmac_hash[-1] & 0xF
        code: int = (
                (hmac_hash[offset] & 0x7F) << 24
                | (hmac_hash[offset + 1] & 0xFF) << 16
                | (hmac_hash[offset + 2] & 0xFF) << 8
                | (hmac_hash[offset + 3] & 0xFF)
        )
        str_code: str = str(10_000_000_000 + (code % 10 ** 6))
        return str_code[-6:]

    @staticmethod
    def int_to_bytestring(i: int, padding: int = 8) -> bytes:
        result = bytearray()
        while i != 0:
            result.append(i & 0xFF)
            i >>= 8
        return bytes(bytearray(reversed(result)).rjust(padding, b"\0"))

    def validate_otp(self, otp: str, for_time: Optional[int] = None, lookback: int = 1) -> bool:
        if for_time is None:
            for_time: int = int(time.time())

        period: int = for_time // self.time_step
        for i in range(0, lookback + 1):
            if otp == self.compute_otp(period - i):
                return True
        return False


if __name__ == "__main__":
    generator = TimeBasedOTPGenerator("konobigguyasarda")
    current_time_period: int = int(time.time()) // 30
    previous_time_period: int = -1

    codes: list[str] = []
    while True:
        time.sleep(1)
        current_time_period = int(time.time()) // 30
        if current_time_period == previous_time_period:
            continue

        previous_time_period = current_time_period
        otp: str = generator.generate_otp(int(time.time()))
        codes.append(otp)
        print(f"Generated OTP: {otp}")

        # Validate OTP
        validate_results: Dict[str, bool] = {code: generator.validate_otp(code) for code in codes}
        print(f"Validating OTP: {validate_results}")
