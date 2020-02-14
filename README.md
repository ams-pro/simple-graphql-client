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
### Executing a query with a file
```python
from simple_graphql_client import GraphQLClient

headers = {'Authorization': 'Bearer ...'}

client = GraphQLClient("https://...", headers=headers)

query = "..."
filename = "..."
variables = {
    ...
}

with open(filename, "rb") as file:
    files = [
        ('1', (filename, file, 'application/pdf'))
    ]

    response = client.query_with_files(query=query, variables=variables, files=files)
```
### Setting a query-specific header
This argument will override the default header which can be set in the `GraphQLClient`
```python
response = client.query(query=query, variables=variables, files=files, headers=headers)
response = client.query_with_files(query=query, variables=variables, files=files, headers=headers)
```