from database_enum import DataBases
from redis_database_service import RedisDatabaseService

class DatabaseServiceFactory:

    def getDatabaseService(self, database_value):
        if database_value == DataBases.REDIS:
            return RedisDatabaseService()
        else:
            raise NotImplementedError