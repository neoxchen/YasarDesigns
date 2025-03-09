from encoder_enum import Encoders
from base_62_encoder import Base62Encoder
from hash_encoder import HashEncoder

class EncoderFactory:

    def getEncoder(self, encoder_value):
        if encoder_value == Encoders.BASE62:
            return Base62Encoder()
        if encoder_value == Encoders.HASH:
            return HashEncoder()