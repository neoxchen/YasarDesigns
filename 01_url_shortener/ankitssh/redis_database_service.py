from abstract_database_service import DatabaseService

class RedisDatabaseService(DatabaseService):
    def __init__(self):
        self.long_url_to_uuid_map = {}
        self.uuid_to_long_url_map = {}
    def save_to_db(self, key, value):
        if key in self.long_url_to_uuid_map:
            return self.long_url_to_uuid_map[key]
        self.long_url_to_uuid_map[key] = value
        self.uuid_to_long_url_map[value] = key
        return value
    def load_from_db(self, key):
        if key not in self.uuid_to_long_url_map:
            return None
        return self.uuid_to_long_url_map[key]