import json

import requests


class Utils:

    @staticmethod
    def getElementsNotRepeated(original_list: list, new_list: list) -> list:

        """
            method to return which elements from new_tags are not in the original_list

            :param original_list -> its a list with the original elements

            :param new_list -> its a list with new elements

            :return list

        """

        data_to_append = []

        for tag in new_list:
            if str(tag).strip() not in original_list:
                data_to_append.append(tag)

        return data_to_append

    @staticmethod
    def cleanEmptyDataDict(dictionary):
        """
            method to clean positions/keys without information in dictionary

            :param dictionary:

        """
        positions_to_delete = []

        for key in dictionary.keys():
            if not dictionary[key]:
                positions_to_delete.append(key)

        for position in positions_to_delete:
            del dictionary[position]

    @staticmethod
    def map_index_to_dict_of_lists(data: list) -> list:
        for position in range(0, len(data)):
            data[position]['index'] = position + 1

        return data

    @staticmethod
    def compose_request(url: str, method: str, headers: dict, body: dict):

        if method.upper() == 'GET':
            return requests.get(url, headers=headers)

        if method.upper() == 'POST':
            return requests.post(url, headers=headers, data=json.dumps(body)).status_code
