from pydantic import BaseModel


class ExplainRequest(BaseModel):
    message: str
