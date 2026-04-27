from pydantic import BaseModel


class AdditionRequest(BaseModel):
    additional_info: str
    additional_number: int


class EntityRequest(BaseModel):
    title: str
    verified: bool
    important_numbers: list[int]
    addition: AdditionRequest
