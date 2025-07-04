from pydantic import BaseModel


class items(BaseModel):
    name : str
    price : str
    count: str