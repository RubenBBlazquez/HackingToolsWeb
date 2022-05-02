import os
from typing import Any
import mysql
from .interface.IDBMethods import IDBMethods
import mysql.connector as mysql_connection


class MySqlBuilder(IDBMethods):

    def __init__(self):
        self.conn = mysql_connection.connect(user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PASSWORD'),
                                             host=os.getenv('MYSQL_HOST'),
                                             database=os.getenv('MYSQL_DATABASE'))

    @staticmethod
    def get_instance():
        return MySqlBuilder()

    def get_connection(self) -> mysql.connector.MySQLConnection:
        return self.conn

    def select_one(self, sql) -> Any:
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        pass

    def select_many(self) -> list:
        pass

    def delete(self) -> Any:
        pass

    def update(self) -> Any:
        pass

    def insert(self, table: str, values: dict) -> None:
        try:

            prepared_data = MySqlBuilder.compound_prepared_sql_query(table, values)
            cursor = self.conn.cursor(prepared=True)
            cursor.execute(prepared_data['sql'], prepared_data['tuple'])
            self.conn.commit()
            cursor.close()

        except mysql.connector.errors.InterfaceError as err:
            print(err)

    @staticmethod
    def compound_prepared_sql_query(table, query_information: dict) -> dict:

        number_of_flags = ''
        fields_flags = ''
        values_flags = ()

        for key in query_information.keys():
            number_of_flags += '%s,'
            fields_flags += key + ','
            values_flags += (query_information[key],)

        number_of_flags = number_of_flags[0:len(number_of_flags) - 1]
        fields_flags = fields_flags[0:len(fields_flags) - 1]

        sql = 'INSERT INTO ' + table + ' (' + fields_flags + ') VALUES (' + number_of_flags + ')'

        print(sql)

        return {'sql': sql, 'tuple': values_flags}
