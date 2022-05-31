from sqlmodel import Field, SQLModel


class Message(SQLModel):
    err: str = Field(..., description='Error code')
    message: str = Field(..., description='Full error message')


responses = {400: {"model": Message}}
