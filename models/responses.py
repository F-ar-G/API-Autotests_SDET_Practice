from pydantic import BaseModel


class AdditionResponse(BaseModel):
    id: int
    additional_info: str
    additional_number: int


class EntityResponse(BaseModel):
    id: int
    title: str
    verified: bool
    important_numbers: list[int]
    addition: AdditionResponse | None = None


class GetAllResponse(BaseModel):
    entity: list[EntityResponse]
