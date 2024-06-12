import strawberry


@strawberry.type
class MessageResponse:
    status: str


@strawberry.input
class MessageInput:
    id: str
    message: str
