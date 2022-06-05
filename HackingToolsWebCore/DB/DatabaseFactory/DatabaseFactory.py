from .interface.IDatabaseFactory import IDatabaseFactory
from ..Databases.interface.IDBMethods import IDBActions
from .Enum.DatabaseTypesEnum import DATABASE_TYPES
from ..Databases.MySqlDB import MySqlDB
from ..Databases.ElasticSearchDB import ElasticSearchDB
from ..Databases.MongoDB import MongoDB


class DatabaseFactory(IDatabaseFactory):
    def get_database(self, db_type: DATABASE_TYPES) -> IDBActions:
        if db_type == DATABASE_TYPES.MYSQL.value:
            return MySqlDB()

        elif db_type == DATABASE_TYPES.MONGO_DB.value:
            return MongoDB()

        elif db_type == DATABASE_TYPES.ELASTICSEARCH.value:
            return ElasticSearchDB()
