import strawberry


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def placeholder(self) -> str:
        return "placeholder"
