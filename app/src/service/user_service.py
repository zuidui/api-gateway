import httpx


async def get_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://user-service:8000/users/{user_id}")
        if response.status_code == 200:
            return response.json()
        return None


async def create_user(name: str, email: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://user-service:8000/users",
            json={"name": name, "email": email, "password": password},
        )
        if response.status_code == 201:
            return response.json()
        return None


async def update_user(user_id: int, name: str, email: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.put(
            f"http://user-service:8000/users/{user_id}",
            json={"name": name, "email": email, "password": password},
        )
        if response.status_code == 200:
            return response.json()
        return None
