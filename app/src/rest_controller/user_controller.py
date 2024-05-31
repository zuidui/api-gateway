from fastapi import APIRouter, HTTPException, status

from graphql_resolver.user_schema import UserInput, UserType

from service.user_service import (
    get_all_users_via_graphql,
    get_user_by_id_via_graphql,
    create_user_via_graphql,
    update_user_via_graphql,
)

user_router = APIRouter()


@user_router.get("/users")
async def get_all_users():
    return await get_all_users_via_graphql()


@user_router.get("/users/{user_id}")
async def get_user_by_id(user_id: int):
    user = await get_user_by_id_via_graphql(user_id)
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@user_router.post("/users")
async def create_user(request: UserInput):
    user = await create_user_via_graphql(request)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="User not created"
    )


@user_router.put("/users/{user_id}")
async def update_user(user_id: int, request: UserInput):
    user = await update_user_via_graphql(
        UserType(
            id=user_id,
            name=request.name,
            email=request.email,
            password=request.password,
        )
    )
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="User not updated"
    )
