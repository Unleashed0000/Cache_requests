from pydantic import BaseModel


class Item(BaseModel):
    key: str
    value: str
