from strawberry.fastapi import GraphQLRouter

from resolver.schema import schema


def graphql_app():
    return GraphQLRouter(schema, path="/graphql")
