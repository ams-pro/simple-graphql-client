# Simple GraphQL Client
## Installation
The client is available on PyPI:
* ``$ pip install simple-graphql-client``
## Usage
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

    response = client.query_with_files(query=query, variables=variables, files=files, headers=headers)
```