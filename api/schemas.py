from pydantic import BaseModel

class RequestInput(BaseModel):
    user_id: str
    user_message: str

class ResponseOutput(BaseModel):
    answer: str