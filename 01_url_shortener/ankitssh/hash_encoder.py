from abstract_url_encoder import Encoder
import hashlib
class HashEncoder(Encoder):

    def encode_url(self, long_url):
        hash = hashlib.new('sha256')
        hash.update(long_url.encode())
        return hash.hexdigest()
