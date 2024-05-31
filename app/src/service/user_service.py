import httpx
from typing import Any, Dict, Optional

from utils.logger import logger_config
from utils.config import get_settings

from graphql_resolver.user_schema import UserType, UserInput

log = logger_config(__name__)
settings = get_settings()


async def send_request(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{settings.USER_SERVICE_URL}", json=payload)
            response.raise_for_status()
            return response.json().get("data")
    except httpx.HTTPStatusError as e:
        log.error(
            f"Request failed with status {e.response.status_code}: {e.response.text}"
        )
    except httpx.RequestError as e:
        log.error(f"An error occurred while requesting {e.request.url!r}.")
    return None


async def send_mutation(mutation: str) -> Optional[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{settings.USER_SERVICE_URL}", json={"query": mutation}
        )
        if response.status_code == 200:
            return response.json()["data"]
        else:
            log.error(
                f"Mutation failed with status {response.status_code}: {response.text}"
            )
            return None


async def get_all_users_via_graphql() -> list[UserType]:
    query = """
    query {
        users {
            id
            name
            email
            password
        }
    }
    """
    data = await send_request({"query": query})
    return [UserType(**user) for user in data["users"]] if data else []


async def get_user_by_id_via_graphql(user_id: int) -> Optional[UserType]:
    query = f"""
    query {{
        user(id: {user_id}) {{
            id
            name
            email
            password
        }}
    }}
    """
    data = await send_request({"query": query})
    return UserType(**data["user"]) if data else None


async def create_user_via_graphql(create_user: UserInput) -> Optional[UserType]:
    mutation = f"""
    mutation {{
        createUser(name: "{create_user.name}", email: "{create_user.email}", password: "{create_user.password}") {{
            id
            name
            email
            password
        }}
    }}
    """
    data = await send_request({"query": mutation})
    return UserType(**data["createUser"]) if data else None


async def update_user_via_graphql(user: UserType) -> Optional[UserType]:
    mutation = f"""
    mutation {{
        updateUser(id: {user.id}, name: "{user.name}", email: "{user.email}", password: "{user.password}") {{
            id
            name
            email
            password
        }}
    }}
    """
    data = await send_request({"query": mutation})
    return UserType(**data["updateUser"]) if data else None
