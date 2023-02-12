import os
from multiprocessing import Lock
from typing import Any
import mysql.connector as mysql
from mysql.connector import MySQLConnection

from HackingToolsWebCore.DB.Databases.interface.IDBMethods import IDBActions
from HackingToolsWebCore.DB.Entities.interface.BaseMethodsEntities import IEntity


class MySqlDB(IDBActions):
    # singleton
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def __init__(self):
        self.conn = mysql.connect(user=os.getenv('MYSQL_USER'),
                                  password=os.getenv('MYSQL_PASSWORD'),
                                  host=os.getenv('MYSQL_HOST'),
                                  database=os.getenv('MYSQL_DATABASE'))

        self.group_functions = ['count', 'sum']

        self.lock = Lock()

    def get_connection(self) -> MySQLConnection:
        return self.conn

    def select_one(self, filter_query: str, entity: IEntity) -> Any:
        cursor = self.conn.cursor()
        cursor.execute(filter_query)

        result = cursor.fetchone()

        return entity.create_object(result).to_dict()

    def select_many(self, select_values: list, prepared_information: dict, entity: IEntity, limit: str,
                    offset: str) -> list:

        self.lock.acquire()

        sql, prepared_values = self.compound_sql_query(select_values, prepared_information, entity, limit, offset)

        entity_list = self.get_result_entity_list(sql, prepared_values, entity)

        self.lock.release()

        return entity_list

    def grouped_select(self, select_values: list, prepared_information: dict, entity: IEntity, limit: str, offset: str):

        self.lock.acquire()

        sql, prepared_values = self.compound_sql_query(select_values, prepared_information, entity, limit, offset,
                                                       True)

        print(sql, prepared_values)

        entity_list = self.get_result_entity_list(sql, prepared_values, entity)

        print(entity_list)

        self.lock.release()

        return entity_list

    def delete(self) -> Any:
        pass

    def update(self) -> Any:
        pass

    def insert(self, entity: IEntity) -> None:
        """

        :param entity: entity from database
        """
        try:

            self.lock.acquire()

            entity_information = entity.to_dict()

            table_name = entity.get_table()

            insert_values = entity_information

            prepared_data = MySqlDB.compound_prepared_insert_sql_query(table_name, insert_values)

            self.conn.reconnect()
            cursor = self.conn.cursor(prepared=True)
            cursor.execute(prepared_data['sql'], prepared_data['tuple'])
            self.conn.commit()

            self.lock.release()

        except mysql.errors.InterfaceError as err:
            self.lock.release()
            print('interface error in mysql -- ', err)

    @staticmethod
    def compound_prepared_insert_sql_query(table: str, prepared_values: dict) -> dict:

        prepared_query_information = MySqlDB.get_prepared_query_information(prepared_values)

        sql = 'INSERT INTO ' + table + ' (' + prepared_query_information['fields_flags'] + ') VALUES ' \
                                                                                           '(' + \
              prepared_query_information['number_of_flags'] + ')'

        print(sql)

        return {'sql': sql, 'tuple': tuple(prepared_values.values())}

    def get_result_entity_list(self, sql: str, prepared_values: tuple, entity: IEntity) -> list:

        self.conn.reconnect()
        cursor = self.conn.cursor(buffered=True)
        cursor.execute(sql, prepared_values)

        columns = [column[0] for column in cursor.description]
        entity_list = []

        for entity_information in cursor.fetchall():
            entity_object = entity.create_object(dict(zip(columns, entity_information))).to_dict().copy()
            entity_list.append(entity_object)

        return entity_list

    def compound_sql_query(self, select_values: list, prepared_information: dict, entity: IEntity, limit: str,
                           offset: str, set_group_information=False) -> tuple:
        sql = 'SELECT '

        if len(select_values) == 0:
            sql += '*'
        else:
            sql += ','.join(list(map(self.prepared_select_values, select_values)))

        sql += ' FROM ' + entity.get_table()

        prepared_values, sql = MySqlDB.compound_where_query(sql, prepared_information)

        if set_group_information:
            sql = self.compound_group_by_query(sql, select_values)

        if limit and offset:
            sql += ' LIMIT %s OFFSET %s'
            prepared_values += (int(limit), int(offset),)

        return sql, prepared_values

    def prepared_select_values(self, element):
        if element not in self.group_functions:
            return element

        return element + '(*) as ' + element

    @staticmethod
    def get_prepared_query_information(prepared_values: dict) -> dict:
        number_of_flags = ''
        fields_flags = ''
        values_flags = ()

        for key in prepared_values.keys():
            number_of_flags += '%s,'
            fields_flags += key + ','
            values_flags += (prepared_values[key],)

        number_of_flags = number_of_flags[0:len(number_of_flags) - 1]
        fields_flags = fields_flags[0:len(fields_flags) - 1]

        return {'number_of_flags': number_of_flags, 'fields_flags': fields_flags}

    @staticmethod
    def compound_where_query(sql: str, prepared_information: dict) -> tuple:
        """

        :param sql:
        :param prepared_information:
        :return:
        """
        prepared_values = tuple()

        if len(prepared_information) > 0:
            sql += ' WHERE '

            for tuple_information in prepared_information:
                field_name = tuple_information[0]
                operator = str(tuple_information[1]).upper()
                field_value = tuple_information[2]

                if field_value:
                    prepared_values += (field_value,)

                    can_set_new_where_operator = len(prepared_values) > 1

                    if type(field_value) == str:
                        sql += ' ' + (operator if can_set_new_where_operator else '') + ' ' + field_name + ' LIKE %s'
                    else:
                        sql += ' ' + (operator if can_set_new_where_operator else '') + ' ' + field_name + ' = %s'

        if len(prepared_values) == 0:
            sql = sql.replace(' WHERE', '')

        return prepared_values, sql

    def compound_group_by_query(self, sql: str, grouped_values: list):
        not_group_functions = list(
            filter(lambda x: 'grp' not in x and x.split('-')[0].lower() not in self.group_functions, grouped_values)
        )

        if len(not_group_functions) > 0:
            sql += ' GROUP BY ' + ','.join(map(lambda x: x.split('-')[0], not_group_functions))

        return sql
