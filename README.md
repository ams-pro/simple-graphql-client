# Simple GraphQL Client
## Installation
The client is available on PyPI:
* ``$ pip install simple-graphql-client``
## Examples
### Executing a query
```python
from simple_graphql_client import GraphQLClient

headers = {'Authorization': 'Bearer ...'}

client = GraphQLClient("https://...", headers=headers)

query = "..."

variables = {
    ...
}
data = client.query(query=query, variables=variables)
```
### Executing a query with a single file
Note: For information visit: https://github.com/jaydenseric/graphql-multipart-request-spec
```python
from simple_graphql_client import GraphQLClient

headers = {'Authorization': 'Bearer ...'}

client = GraphQLClient("https://...", headers=headers)

query = "..."
filename = "..."
variables = {
    ...
    'file': None,
    ...
}

with open(filename, "rb") as file:
    files = [
        ('file', (filename, file))
    ]

    response = client.query_with_files(query=query, variables=variables, files=files)
```
### Executing a query with a multiple files
```python
from simple_graphql_client import GraphQLClient

client = GraphQLClient("https://...")

query = "..."
filenames = ["...", "..."]
files = []
variables = {
    ...
    'files': [None, None]
    ... 
}

for i, filename in enumerate(filenames):
    variable = 'files.{}'.format(i)
    files.append((variable, (filename, open(filename, "rb"))))

response = client.query_with_files(query=query, variables=variables, files=files)
```
### Setting a query-specific header
This argument will override the default header which can be set in the `GraphQLClient`
```python
response = client.query(query=query, variables=variables, files=files, headers=headers)
response = client.query_with_files(query=query, variables=variables, files=files, headers=headers)
```