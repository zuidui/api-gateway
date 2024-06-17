import strawberry


@strawberry.type
class Query:
    @strawberry.field
    def placeholder(self) -> str:
        return "placeholder"
