from strawberry import Schema
from strawberry.fastapi import GraphQLRouter

from resolvers.user_query import UserQuery
from resolvers.user_mutation import UserMutation


def graphql_app():
    schema = Schema(query=(UserQuery), mutation=(UserMutation))
    return GraphQLRouter(schema, path="/graphql")
