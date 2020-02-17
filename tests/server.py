from flask import Flask
from graphene_file_upload.flask import FileUploadGraphQLView
from schema import schema

app = Flask(__name__)
app.debug = True
app.add_url_rule('/graphql', view_func=FileUploadGraphQLView.as_view('graphql', schema=schema, graphiql=app.debug))

if __name__ == "__main__":
    app.run()
