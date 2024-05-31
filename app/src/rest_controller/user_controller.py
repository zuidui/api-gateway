from fastapi import APIRouter, HTTPException, status
from graphql_resolver.user_schema import UserInput, UserType
from service.user_service import (
    get_all_users_via_graphql,
    get_user_by_id_via_graphql,
    create_user_via_graphql,
    update_user_via_graphql,
)
from utils.logger import logger_config

log = logger_config(__name__)
user_router = APIRouter()


@user_router.get("/users")
async def get_all_users():
    log.info("Fetching all users")
    users = await get_all_users_via_graphql()
    log.info(f"Fetched users: {users}")
    return users


@user_router.get("/users/{user_id}")
async def get_user_by_id(user_id: int):
    log.info(f"Fetching user with id: {user_id}")
    user = await get_user_by_id_via_graphql(user_id)
    if user:
        log.info(f"User found: {user}")
        return user
    log.warning(f"User with id {user_id} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@user_router.post("/users")
async def create_user(request: UserInput):
    log.info(f"Creating user with data: {request}")
    user_created = await create_user_via_graphql(request)
    if user_created:
        log.info(f"User created: {user_created}")
        return user_created
    log.error("Failed to create user")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="User not created"
    )


@user_router.put("/users/{user_id}")
async def update_user(user_id: int, request: UserInput):
    log.info(f"Updating user with id {user_id} with data: {request}")
    user_updated = await update_user_via_graphql(
        UserType(
            id=user_id,
            name=request.name,
            email=request.email,
            password=request.password,
        )
    )
    if user_updated:
        log.info(f"User updated: {user_updated}")
        return user_updated
    log.error(f"Failed to update user with id {user_id}")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="User not updated"
    )
