import json

import requests
from graphql import parse
from graphql.language.ast import ListType


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

    def query_with_files(self, query: str, variables: dict, files: list, headers: dict = None):
        if headers is None:
            headers = self._HEADERS

        upload_fields, operation_name = self._get_upload_fields(query)

        _map = {}

        for (field_name, is_list) in upload_fields:
            if is_list:

                assert len(variables[field_name]) == len(files), \
                    "Not enough values for either '{}' or '{}' in variables".format(field_name, field_name)

                for i, file in enumerate(files):
                    # validate variables
                    assert variables[field_name][i] is None, "No null value for {} at index {}".format(field_name, i)

                    _map[file[0]] = ['variables.{}.{}'.format(field_name, i)]
            else:
                # validate variables
                assert variables[field_name] is None, "No null value for {}".format(field_name)
                files = [files]
                _map[field_name] = ['variables.{}'.format(field_name)]

        _operations = {
            'operationName': operation_name,
            'query': query,
            'variables': variables
        }

        payload = {
            'operations': json.dumps(_operations),
            'map': json.dumps(_map)
        }

        response_json = self._make_request(query=query, payload=payload, headers=headers, files=files)
        return response_json

    @staticmethod
    def _get_upload_fields(query):

        upload_fields = []

        parsed = parse(query)
        variables = parsed.definitions[0].variable_definitions
        for variable in variables:
            # get type depth
            is_list = False
            _type = variable.type
            while True:
                if isinstance(_type, ListType) and not is_list:
                    is_list = True
                try:
                    new_type = _type.type
                except AttributeError:
                    break
                _type = new_type

            if _type.name.value == "Upload":
                variable_name = variable.variable.name.value
                upload_fields.append((variable_name, is_list))
            else:
                continue

        operation_name = parsed.definitions[0].name.value
        return upload_fields, operation_name

    def _make_request(self, query: str, headers: dict = None, payload: dict = None, json: dict = None,
                      files: list = None):
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
