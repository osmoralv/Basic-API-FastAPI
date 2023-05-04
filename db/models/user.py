from pydantic import BaseModel


class User(BaseModel):
    id: str | None
    name: str
    surname: str
    age: int
    username: str
    email: str

    