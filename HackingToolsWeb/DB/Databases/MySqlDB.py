import os
from multiprocessing import Lock
from typing import Any
import mysql
from HackingToolsWeb.DB.Databases.interface.IDBMethods import IDBActions
import mysql.connector as mysql_connection
from HackingToolsWeb.DB.Entities.interface.BaseMethodsEntities import IEntity


class MySqlDB(IDBActions):
    # singleton
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.conn = mysql_connection.connect(user=os.getenv('MYSQL_USER'),
                                             password=os.getenv('MYSQL_PASSWORD'),
                                             host=os.getenv('MYSQL_HOST'),
                                             database=os.getenv('MYSQL_DATABASE'))

        self.lock = Lock()

    def get_connection(self) -> mysql.connector.MySQLConnection:
        return self.conn

    def select_one(self, filter_query: str, entity: IEntity) -> Any:
        cursor = self.conn.cursor()
        cursor.execute(filter_query)

        result = cursor.fetchall()

        return entity.create_object(result).to_dict()

    def select_many(self) -> list:
        pass

    def delete(self) -> Any:
        pass

    def update(self) -> Any:
        pass

    def insert(self, entity: IEntity) -> None:
        try:

            self.lock.acquire()

            entity_information = entity.to_dict()

            table_name = entity_information['TABLE_NAME']
            del entity_information['TABLE_NAME']

            insert_values = entity_information

            prepared_data = MySqlDB.compound_prepared_sql_query(table_name, insert_values)

            self.conn.reconnect()
            cursor = self.conn.cursor(prepared=True)
            cursor.execute(prepared_data['sql'], prepared_data['tuple'])
            self.conn.commit()

            self.lock.release()

        except mysql.connector.errors.InterfaceError as err:
            self.lock.release()
            print('interface error in mysql -- ', err)

    @staticmethod
    def compound_prepared_sql_query(table: str, insert_values: dict) -> dict:

        number_of_flags = ''
        fields_flags = ''
        values_flags = ()

        for key in insert_values.keys():
            number_of_flags += '%s,'
            fields_flags += key + ','
            values_flags += (insert_values[key],)

        number_of_flags = number_of_flags[0:len(number_of_flags) - 1]
        fields_flags = fields_flags[0:len(fields_flags) - 1]

        sql = 'INSERT INTO ' + table + ' (' + fields_flags + ') VALUES (' + number_of_flags + ')'

        print(sql)

        return {'sql': sql, 'tuple': values_flags}
