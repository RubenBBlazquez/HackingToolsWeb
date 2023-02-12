import json
import os
from typing import Any

from bson import json_util

from HackingToolsWebCore.DB.Databases.interface.IDBMethods import IDBActions
from HackingToolsWebCore.DB.Entities.interface.BaseMethodsEntities import IEntity
import pymongo

from HackingToolsWebCore.Utils.Utils import Utils


class MongoDB(IDBActions):

    def __init__(self):
        self.mongoDBClient = pymongo.MongoClient(os.getenv("MONGO_CONNECTION_URL"))
        self.database = self.mongoDBClient.get_database(os.getenv('MONGO_DATABASE'))
        self.group_values = ['count']

    # singleton
    _instance = None

    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        return cls._instance

    def get_connection(self) -> Any:
        return self.mongoDBClient

    def select_one(self, filter_query: str, entity: IEntity) -> Any:
        collection = self.database.get_collection(entity.get_table())

        return collection.find_one(filter_query)

    def select_many(self, select_values: list, query_values: list[tuple], entity: IEntity, limit: str,
                    offset: str) -> list:
        collection = self.database.get_collection(entity.get_table())

        return json.loads(json_util.dumps(
            collection.find(MongoDB.compose_basic_mongo_query(query_values))
        ))

    def grouped_select(self, select_values: list, query_values: list[tuple], entity: IEntity, limit: str,
                       offset: str) -> list:
        collection = self.database.get_collection(entity.get_table())
        aggregate_condition = self.compose_group_by_aggregate_query(select_values, query_values)
        cursor = list(collection.aggregate(aggregate_condition))

        for element in cursor:
            for key in element['_id'].keys():
                element[key] = element['_id'][key]

            del element['_id']

        return json.loads(json_util.dumps(cursor))

    def delete(self) -> Any:
        pass

    def update(self) -> Any:
        pass

    def insert(self, entity: IEntity) -> bool:
        collection = self.database.get_collection(entity.get_table())
        is_entity_already_added = len(list(collection.find(entity.to_dict()))) != 0

        if is_entity_already_added:
            return False

        inserted_id = collection.insert_one(entity.to_dict()).inserted_id

        return inserted_id is not None

    @staticmethod
    def compose_basic_mongo_query(query_information: list[tuple]):
        query_dict = {}

        for query in query_information:
            field_name = query[0]
            logical_operator = query[1]
            value = query[2]

            condition = {field_name: value}

            if logical_operator not in query_dict.keys():
                query_dict[logical_operator] = [condition]
                continue

            query_dict[logical_operator].append(condition)

    def compose_group_by_aggregate_query(self, select_values: list, query_values: list[tuple]) -> list[dict]:
        aggregate_condition = []
        group_condition = {'$group': {'_id': {}}}
        match_condition = {'$match': {}}

        for query_value in query_values:
            field_name, logical_operator, field_value = query_value
            condition = {field_name: field_value}

            if not field_value:
                continue

            if logical_operator not in match_condition['$match']:
                match_condition['$match'][logical_operator] = [condition]
                continue

            match_condition['$match'][logical_operator].append(condition)

        aggregate_condition.append(match_condition)

        for select_value in select_values:
            if select_value in self.group_values:
                group_condition['$group'][select_value] = {'$sum': 1}

                continue

            group_condition['$group']['_id'][select_value] = '$' + str(select_value)

        aggregate_condition.append(group_condition)

        return aggregate_condition
