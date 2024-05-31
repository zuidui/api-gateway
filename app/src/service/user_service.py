import httpx
from typing import Any, Dict, Optional

from utils.logger import logger_config
from utils.config import get_settings

from graphql_resolver.user_schema import UserType, UserInput

log = logger_config(__name__)
settings = get_settings()


async def send_request(payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        log.debug(
            f"Sending request to {settings.USER_SERVICE_URL} with payload: {payload}"
        )
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{settings.USER_SERVICE_URL}", json=payload)
            response.raise_for_status()
            log.debug(f"Response received: {response.json()}")
            return response.json().get("data")
    except httpx.HTTPStatusError as e:
        log.error(
            f"Request failed with status {e.response.status_code}: {e.response.text}"
        )
    except httpx.RequestError as e:
        log.error(f"An error occurred while requesting {e.request.url!r}.")
    except Exception as e:
        log.error(f"Unexpected error: {e}")
    return None


async def get_all_users_via_graphql() -> list[UserType]:
    query = """
    query {
        get_all {
            id
            name
            email
            password
        }
    }
    """
    log.debug(f"Query: {query}")
    data = await send_request({"query": query})
    users = [UserType(**user) for user in data["get_all"]] if data else []
    log.debug(f"Retrieved users: {users}")
    return users


# FIX: Why cannot use user_id instead of userId on the query?
async def get_user_by_id_via_graphql(user_id: int) -> Optional[UserType]:
    query = f"""
    query {{
        get_by_id (userId: {user_id}) {{
            id
            name
            email
            password
        }}
    }}
    """
    log.debug(f"Query: {query}")
    data = await send_request({"query": query})
    user = UserType(**data["get_by_id"]) if data else None
    log.debug(f"Retrieved user: {user}")
    return user


async def create_user_via_graphql(create_user: UserInput) -> Optional[UserType]:
    mutation = f"""
    mutation {{
        create (name: "{create_user.name}", email: "{create_user.email}", password: "{create_user.password}") {{
            id
            name
            email
            password
        }}
    }}
    """
    log.debug(f"Mutation: {mutation}")
    data = await send_request({"query": mutation})
    user_created = UserType(**data["create"]) if data else None
    log.debug(f"User created: {user_created}")
    return user_created


# FIX: Why cannot use user_id instead of userId on the query?
async def update_user_via_graphql(user: UserType) -> Optional[UserType]:
    mutation = f"""
    mutation {{
        update (userId: {user.id}, name: "{user.name}", email: "{user.email}", password: "{user.password}") {{
            id
            name
            email
            password
        }}
    }}
    """
    log.debug(f"Mutation: {mutation}")
    data = await send_request({"query": mutation})
    user_updated = UserType(**data["update"]) if data else None
    log.debug(f"User updated: {user_updated}")
    return user_updated
