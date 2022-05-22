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