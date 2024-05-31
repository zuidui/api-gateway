import strawberry
from typing import Optional

from graphql_resolver.user_schema import UserType, UserInput

from service.user_service import create_user_via_graphql, update_user_via_graphql


@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def create_user(self, new_user: UserInput) -> Optional[UserType]:
        return await create_user_via_graphql(new_user)

    @strawberry.mutation
    async def update_user(
        self, user_id: int, user_data: UserInput
    ) -> Optional[UserType]:
        return await update_user_via_graphql(UserType(id=user_id, **user_data.__dict__))
