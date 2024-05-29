import strawberry
from typing import Optional

from schema.user_schema import UserType
from service.user_service import create_user, update_user


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_user(
        self, name: str, email: str, password: str
    ) -> Optional[UserType]:
        user_data = await create_user(name, email, password)
        if user_data:
            return UserType(
                id=user_data["id"],
                name=user_data["name"],
                email=user_data["email"],
                password=user_data["password"],
            )
        return None

    @strawberry.mutation
    async def update_user(
        self, id: int, name: str, email: str, password: str
    ) -> Optional[UserType]:
        user_data = await update_user(id, name, email, password)
        if user_data:
            return UserType(
                id=user_data["id"],
                name=user_data["name"],
                email=user_data["email"],
                password=user_data["password"],
            )
        return None
