from encoder_enum import Encoders
from database_enum import DataBases
from encoder_factory import EncoderFactory
from database_service_factory import DatabaseServiceFactory
class UrlService:
    BASE_URL = "tinywiggle.com"
    
    def __init__(self, encoder_value=Encoders.BASE62, database_value=DataBases.REDIS):
        self.long_url_to_uuid_map = {}
        self.uuid_to_long_url_map = {}
        self.encoder_factory = EncoderFactory().getEncoder(encoder_value)
        self.database_factory = DatabaseServiceFactory().getDatabaseService(DataBases.REDIS)
        

    def shorten_url(self, long_url):
        uuid = self.encoder_factory.encode_url(long_url)
        uuid = self.database_factory.save_to_db(long_url, uuid)
        if uuid:
            return self.__build_short_url(uuid)
        uuid = self.encoder_factory.encode_url(long_url)
        uuid = self.database_factory.save_to_db(long_url, uuid)
        return self.__build_short_url(uuid)
        # # If the long url has already been converted
        # if long_url in self.long_url_to_uuid_map:
        #     uuid = self.long_url_to_uuid_map.get(long_url)
        #     return self.__build_short_url(uuid)
        
        # # If long url is seen firt time
        # uuid = self.encoder_factory.encode_url(long_url)
        # self.long_url_to_uuid_map[long_url] = uuid
        # self.uuid_to_long_url_map[uuid] = long_url

        # return self.__build_short_url(uuid)

    def get_long_url(self, short_url):
        uuid = self.__extract_uuid_from_short_url(short_url)
        long_url = self.database_factory.load_from_db(uuid)
        if long_url:
            return long_url
        # uuid = self.__extract_uuid_from_short_url(short_url)
        # if uuid in self.uuid_to_long_url_map:
        #     return self.uuid_to_long_url_map[uuid]
        
        return "404: Not Found"
    # Private helper functions


    def __build_short_url(self, uuid):
        return "/".join([self.BASE_URL, uuid])
    
    def __extract_uuid_from_short_url(self, short_url):
        return short_url.split(self.BASE_URL + "/")[-1]

    


