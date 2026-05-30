from pydantic import BaseModel, EmailStr


class JiraConnectRequest(BaseModel):
    connectionName: str
    baseUrl: str
    email: EmailStr
    apiToken: str
