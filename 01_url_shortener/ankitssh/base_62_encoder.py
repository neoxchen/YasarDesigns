from abstract_url_encoder import Encoder
import time
class Base62Encoder(Encoder):
    BASE_62_MAP = {}

    def __init__(self):
        self.__build_base_62_map()
    
    def encode_url(self, long_url):
        epoch_time = self.__get_epoch_time()
        uuid = self.__convert_epoch_to_uuid(epoch_time)
        return uuid

    def __build_base_62_map(self):
        counter = 0
        for i in range(10):
            self.BASE_62_MAP[counter] = str(i)
            counter+=1
        for i in range(26):
            self.BASE_62_MAP[counter] = chr(ord('A') + i)
            counter+=1
        for i in range(26):
            self.BASE_62_MAP[counter] = chr(ord('a') + i)
            counter+=1
    
    def __convert_epoch_to_uuid(self, epoch_time):
        uuid_array = []
        while(epoch_time):
            remainder = epoch_time % 62
            uuid_array.append(self.BASE_62_MAP[remainder])
            epoch_time = epoch_time // 62
        return "".join(uuid_array[::-1])

    def __get_epoch_time(self):
        return int(time.time())