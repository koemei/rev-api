import requests
import logging
logging.basicConfig()
import traceback
import pprint
import json
from rev.auth import RevAuth
from rev.utils import read_settings_file
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

        # setup settings
        self.settings = read_settings_file()

        # setup logger
        self.log = logging.getLogger(__name__)
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

    def request_get(self, url, params={}, headers={}, stream=False):
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
            auth=RevAuth(client_api_key=self._client_api_key, user_api_key=self._user_api_key),
            headers=headers,
            stream=stream
        )
        self.verify_response(response)
        if not stream:
            return response.json()
        else:
            return response

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
        if not response.status_code == requests.codes.ok and response.status_code != 201:
            log = logging.getLogger()
            log.error("Error executing query!")
            log.error(response.__dict__)
            response.raise_for_status()