import strawberry
from typing import Optional, List

from resolvers.user_schema import UserType

from services.user_service import (
    get_all_users_via_graphql as get_all_users,
    get_user_by_id_via_graphql as get_user_by_id,
)


@strawberry.type
class UserQuery:
    users: List[UserType] = strawberry.field(resolver=get_all_users)
    user: Optional[UserType] = strawberry.field(resolver=get_user_by_id)
