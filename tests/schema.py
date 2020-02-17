from graphene import ObjectType, String, Schema, Mutation, Boolean, List
from graphene_file_upload.scalars import Upload


class Query(ObjectType):
    hello_world = String(variable=String())
    error = String()

    def resolve_hello_world(self, info, variable, **kwargs):
        return "Hello World {}".format(variable)

    def resolve_error(self, info, **kwargs):
        raise Exception("Testing Exceptions")


class UploadFile(Mutation):
    success = Boolean()
    first_line = String()

    class Arguments:
        file = Upload(required=True)

    def mutate(self, info, file, **kwargs):
        first_line = file.readline().strip().decode('utf-8')
        file.seek(0)
        return UploadFile(success=True, first_line=first_line)


class UploadFiles(Mutation):
    success = Boolean()
    first_lines = List(String)

    class Arguments:
        files = List(Upload, required=True)

    def mutate(self, info, files, **kwargs):
        first_lines = []
        for file in files:
            first_line = file.readline().strip().decode('utf-8')
            first_lines.append(first_line)
            file.seek(0)
        return UploadFiles(success=True, first_lines=first_lines)


class Mutation(ObjectType):
    upload_file = UploadFile.Field()
    upload_files = UploadFiles.Field()


schema = Schema(query=Query, mutation=Mutation)
