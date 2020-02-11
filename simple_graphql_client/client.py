import json

import requests

SUBDIR = None
GRAPHQL_FILE_PATH = ''
HEADERS = {}


class GraphQLClient:
    _BASE_URL = None
    _HEADERS = {}

    def __init__(self, base_url, headers=None):
        if headers is None:
            headers = {}

        self._BASE_URL = base_url
        self._HEADERS = headers

    def query(self, query: str, variables: dict = None, headers: dict = None):
        if variables is None:
            variables = {}
        if headers is None:
            headers = self._HEADERS

        _json = {'query': query, 'variables': variables}
        response_json = self._make_request(query=query, headers=headers, json=_json)
        return response_json

    def query_with_files(self, query: str, variables: dict = None, headers: dict = None, files: dict = None):
        if files is None:
            files = {}
        if variables is None:
            variables = {}
        if headers is None:
            headers = self._HEADERS

        _operations = {
            'operationName': None,  # todo get operations name dynamic
            'query': query,
            'variables': variables
        }

        # Todo build file map dynamic
        _map = {'1': ['variables.file.0']}

        payload = {
            'operations': json.dumps(_operations),
            'map': json.dumps(_map)
        }

        response_json = self._make_request(query=query, payload=payload, headers=headers, files=files)
        return response_json

    def _make_request(self, query: str, headers: dict = None, payload: dict = None, json: dict = None,
                      files: dict = None):
        request = requests.post(self._BASE_URL, headers=headers, data=payload, files=files, json=json)
        if request.status_code == 200:
            if 'errors' in request.json().keys():
                raise Exception("[ERROR] Bad Request: {}. \n {}".format(request.json()['errors'], query))
            return request.json()
        else:
            if 400 <= request.status_code < 500:
                raise Exception("[ERROR] Bad Request: {}. \n {}".format(request.content, query))
            else:
                raise Exception("[ERROR] failed to run by returning error of {}. {}".format(request.status_code, query))
