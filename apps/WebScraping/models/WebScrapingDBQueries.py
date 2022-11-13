import json

from HackingToolsWebCore.DB.Entities.LogsWebScraping.LogsWebScraping import LogsWebScraping
from HackingToolsWebCore.DB.Entities.TagScrapped.GroupedTagsScrapped import GroupedTagsScrapped
from HackingToolsWebCore.DB.Entities.TagScrapped.TagScrapped import TagScrapped
from HackingToolsWebCore.DB.Entities.WebScrapped.WebScrapped import WebScrapped
from HackingToolsWebCore.Utils.Utils import Utils
from HackingToolsWebCore.settings import Database, serverCache
from apps.WebScraping.models.BaseWebScraping import WebScraping, WEB_SCRAPING_CACHE_KEYS


class WebScrapingQueries:

    @staticmethod
    def add_new_data_to_db(identifier: str, tags_list: list, base_url: str, endpoint: str) -> None:
        """
            Method to append the new data to tags scrapped

            :param: endpoint:
            :param base_url:
            :param identifier -> it's a key to set in the tags_scrapped dictionary
            :param tags_list -> it's the data to set to tags_scrapped with the identifier passed by parameter

        """

        tags_information = WebScraping.get_tags_information(identifier, tags_list)
        tags_not_repeated = tags_information['tagsNotRepeated']
        tags_already_scrapped = tags_information['tagsAlreadyScrapped']

        serverCache.put(WEB_SCRAPING_CACHE_KEYS.TAGS_SCRAPPED.value, tags_already_scrapped)

        for element in tags_not_repeated:
            try:
                entity = TagScrapped() \
                    .setTag(identifier).setTagInfo(element) \
                    .setWebScrapped(base_url) \
                    .setEndpointWebScrapped(endpoint)

                Database.insert(entity)

            except Exception as ex:
                WebScrapingQueries.insert_log(ex.args, base_url, endpoint)

    @staticmethod
    def insert_log(message, base_url: str, endpoint: str):
        """
            Method to insert an error in DB

            :param endpoint:
            :param base_url:
            :param message: error message to insert in database
        """

        Database.insert(
            LogsWebScraping()
            .setLogError(message)
            .setBaseUrl(base_url)
            .setEndpoint(endpoint))

    @staticmethod
    def get_tags_information_from_web_scrapped(
            base_url: str,
            endpoint: str,
            tag: str,
            limit: str,
            offset: str,
            search_value: str
    ) -> list:
        """
            sql query to get information about tags already scraped

            :param base_url:
            :param endpoint:
            :param tag:
            :param limit:
            :param offset:
            :param search_value:

            :return: list
        """

        entity = TagScrapped()
        select_values = entity.to_dict().keys()
        attribute_literals = entity.get_attributes_enum()

        query_values = [
            (attribute_literals.WEB_SCRAPPED.value, 'and', base_url.strip()),
            (attribute_literals.ENDPOINT_WEB_SCRAPPED.value, 'and', endpoint.strip()),
            (attribute_literals.TAG.value, 'and', tag.strip()),
        ]

        tags = Database.select_many(select_values, query_values, entity, limit, offset)

        return Utils.map_index_to_dict_of_lists(tags)

    @staticmethod
    def get_grouped_tag_count_from_web_scrapped(base_url: str, endpoint: str, limit: str, offset: str,
                                                search_value: str) -> list:
        """
            method to get grouped tags from webs scrapped

            :param: search_value:
            :param search_value: value to find webs with a name that contains this
            :param limit: limit of values to get from db
            :param offset: start position of values
            :param base_url: from web scrapped
            :param endpoint: from web scrapped

            :return: list:
        """

        entity = GroupedTagsScrapped()

        select_values = entity.to_dict().keys()
        attribute_literals = entity.get_attributes_enum()

        query_values = [
            (attribute_literals.WEB_SCRAPPED.value, 'and', base_url),
            (attribute_literals.ENDPOINT_WEB_SCRAPPED.value, 'and', endpoint),
            (attribute_literals.WEB_SCRAPPED.value, 'or', search_value),
            (attribute_literals.ENDPOINT_WEB_SCRAPPED.value, 'or', search_value),
            (attribute_literals.TAG.value, 'or', search_value)
        ]

        tags = Database.grouped_select(select_values, query_values, entity, limit, offset)

        return Utils.map_index_to_dict_of_lists(tags)

    @staticmethod
    def get_information_from_web_scrapped() -> list:
        """
            method to get all webs already scrapped

            return list:
        """

        return Database.select_many([], dict(), WebScrapped(), '', '')

    @staticmethod
    def get_information_by_action(tags_data_file, action, base_url, tag, endpoint, limit, offset, search_value) -> dict:

        response_information = {}

        if action == 'TAGS_INFORMATION':
            response_information = json.load(open(tags_data_file, "r"))

        if action == 'TAGS_FROM_WEBS_SCRAPPED_INFORMATION_GROUPED':
            result = WebScrapingQueries.get_grouped_tag_count_from_web_scrapped(
                base_url,
                endpoint,
                limit,
                offset,
                search_value
            )

            total_results = WebScrapingQueries.get_grouped_tag_count_from_web_scrapped(
                base_url,
                endpoint,
                '',
                '',
                search_value
            )

            response_information = {
                'recordsTotal': len(total_results),
                'recordsFiltered': total_results,
                'data': result
            }

        if action == 'TAGS_FROM_WEBS_SCRAPPED_INFORMATION':
            records = WebScrapingQueries.get_tags_information_from_web_scrapped(
                base_url,
                endpoint,
                tag,
                limit,
                offset,
                search_value
            )

            total_records = WebScrapingQueries.get_tags_information_from_web_scrapped(
                base_url,
                endpoint,
                tag,
                limit='',
                offset='',
                search_value=''
            )

            response_information = {
                'recordsTotal': len(total_records),
                'recordsFiltered': total_records,
                'data': records
            }

        if action == 'WEBS_SCRAPPED_INFORMATION':
            response_information = {'data': WebScrapingQueries.get_information_from_web_scrapped()}

        return response_information

