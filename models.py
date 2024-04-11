from pydantic import BaseModel


class Room(BaseModel):
    name: str


class Temperature(BaseModel):
    temperature: float
    room_id: int
    date: str = None
