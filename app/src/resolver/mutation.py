import strawberry


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def placehold(self) -> str:
        return "placeholder"
