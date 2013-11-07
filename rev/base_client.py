import requests
import logging
logging.basicConfig()
import os
import traceback
import pprint
import json

from ConfigParser import SafeConfigParser
from ConfigParser import Error as ConfigParserError

from rev.exceptions import SettingsFileNotFoundError
from rev.auth import RevAuth
from copy import copy

pp = pprint.PrettyPrinter(indent=4)


class BaseClient(object):
    """
    This is the base client, implements basic rest methods
    """

    def __init__(self):
        """
        Create the api client
        """

        # setup logger
        self.log = logging.getLogger(__name__)
        self.log.setLevel('DEBUG')

        # read settings
        settings_file_path = "settings.ini"
        try:
            if os.path.exists(settings_file_path):
                self.settings = SafeConfigParser()
                self.settings.read(settings_file_path)
            else:
                raise SettingsFileNotFoundError("Settings file not found, please copy settings.example.ini to settings.ini and fill in your details")
        except ConfigParserError, e:
            self.log.error("Error parsing settings file")
            self.log.error(e)
            self.log.error(traceback.format_exc())
            raise e

        self.log.setLevel(self.settings.get('logging', 'level'))

        # init config
        try:
            self._user_api_key = self.settings.get("credentials", "user_api_key")
            self._client_api_key = self.settings.get("credentials", "client_api_key")
        except Exception,e:
            self.log.error("Error getting api_key from settings file")
            self.log.error(e)
            self.log.error(traceback.format_exc())
            raise e

        try:
            self.base_path = self.settings.get("base", "paths.api")
        except Exception,e:
            self.log.error("Error getting api path from settings file")
            self.log.error(e)
            self.log.error(traceback.format_exc())
            raise e

        self.response = None

    def path(self, args):
        """
        Build path for api call
        @params url path params
        """
        try:
            path_array = copy(args)
            path_array.reverse()
            path_array.append(self.base_path)
            path_array.reverse()
            path = '/'.join(path_array)
            return path
        except Exception, e:
            self.log.error("Error building path with params:")
            self.log.error(args)
            self.log.error(e)
            self.log.error(traceback.format_exc())
            raise

    def request_get(self, url, params={}):
        """
        GET call at the given url
        @params url: the path to the method to call, relative to the api root url
        @params params: dictionary containing the parameters for the rest call
        @return rest response in json
        """
        self.log.debug("Making GET request to %s" % self.path(url))
        response = requests.get(
            url=self.path(url),
            params=params,
            auth=RevAuth(client_api_key=self._client_api_key, user_api_key=self._user_api_key)
        )
        self.verify_response(response)
        return response.json()

    def request_post(self, url, params={}):
        """
        POST call at the given url
        @params url: the path to the method to call, relative to the api root url
        @params params: dictionary containing the post parameters for the rest call
        @return rest response in json
        """
        self.log.debug("Making POST request to %s" % self.path(url))
        response = requests.post(
            url=self.path(url),
            data=json.dumps(params),
            auth=RevAuth(client_api_key=self._client_api_key, user_api_key=self._user_api_key),
            headers={'Content-Type': 'application/json'}
        )
        self.verify_response(response)
        return response

    @classmethod
    def verify_response(cls, response):
        """
        Raises exception if response is not considered as success

        @param response [HTTPParty::Response] HTTParty response obj. Net::HTTPResponse represented by .response
        @return [Boolean] true if response is considered as successful
        """

        # HTTP response codes are handled here and propagated up to the caller, since caller should be able
        # to handle all types of errors the same - using exceptions
        if not response.status_code == requests.codes.ok:
            print response._content
            response.raise_for_status()