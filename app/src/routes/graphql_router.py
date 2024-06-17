from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter

from resolver.schema import schema


def graphql_app():
    return GraphQLRouter(schema, path="/graphql")


graphql_router = APIRouter()


@graphql_router.get(
    "/schema", tags=["Sanity check"], responses={200: {"description": "Get the schema"}}
)
def get_schema():
    return schema.as_str()
