from pydantic import BaseModel
from typing import Any

class SuccessResponse(BaseModel):
    message: str = "Success"
    status: str = "success"
    data: Any = None
