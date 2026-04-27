from models.requests import AdditionRequest, EntityRequest


class EntityRequestBuilder:
    def __init__(self):
        self._title: str = ""
        self._verified: bool = False
        self._important_numbers: list[int] = []
        self._addition: AdditionRequest | None = None

    def title(self, value: str) -> "EntityRequestBuilder":
        self._title = value
        return self

    def verified(self, value: bool) -> "EntityRequestBuilder":
        self._verified = value
        return self

    def important_numbers(self, value: list[int]) -> "EntityRequestBuilder":
        self._important_numbers = value
        return self

    def addition(self, info: str, number: int) -> "EntityRequestBuilder":
        self._addition = AdditionRequest(
            additional_info=info,
            additional_number=number,
        )
        return self

    def build(self) -> EntityRequest:
        if self._addition is None:
            raise ValueError("Не вызван .addition() — поле обязательно перед build()")
        return EntityRequest(
            title=self._title,
            verified=self._verified,
            important_numbers=self._important_numbers,
            addition=self._addition,
        )
