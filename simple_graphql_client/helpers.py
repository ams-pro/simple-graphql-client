def load(path):
    with open(path) as file:
        gql = file.read()

    return gql
