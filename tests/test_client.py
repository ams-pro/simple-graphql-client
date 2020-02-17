from simple_graphql_client import GraphQLClient

client = GraphQLClient("http://localhost:5000/graphql")


def test_query():
    query = """
    query helloWorld($variable: String) {
        helloWorld(variable: $variable)
    }
    """

    variables = {
        "variable": "Fabian"
    }
    response = client.query(query=query, variables=variables)
    assert "data" in response.keys(), "Error received"
    assert "Hello World Fabian" in response["data"]["helloWorld"], "Received incorrect response"


def test_query_with_file():
    query = """
    mutation uploadFile($file: Upload!) {
        uploadFile(file: $file) {
            success
            firstLine
        }
    }
    """
    filename = "test.txt"
    variables = {'file': None}
    with open(filename, "rb") as file:
        files = ('file', (filename, file))

        response = client.query_with_files(query=query, variables=variables, files=files)
        assert "data" in response.keys(), "Error received"
        assert "Hello World" == response['data']['uploadFile']['firstLine'], "Received incorrect response"


def test_query_with_files():
    query = """
    mutation uploadFiles($files: [Upload]!) {
        uploadFiles(files: $files) {
            success
            firstLines
        }
    }
    """
    filenames = ["test.txt", "test.txt"]
    files = []
    variables = {'files': [None, None]}

    for i, filename in enumerate(filenames):
        variable = 'files.{}'.format(i)
        files.append((variable, (filename, open(filename, "rb"))))

    response = client.query_with_files(query=query, variables=variables, files=files)

    assert "data" in response.keys(), "Error received"
    assert ["Hello World", "Hello World"] == response['data']['uploadFiles'][
        'firstLines'], "Received incorrect response"


test_query()
test_query_with_file()
test_query_with_files()
