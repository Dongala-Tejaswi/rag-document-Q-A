from pydantic import BaseModel

class QuestionRequest(BaseModel):
    query: str

class QuestionResponse(BaseModel):
    answer: str

class UploadResponse(BaseModel):
    message: str