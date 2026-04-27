import pytest

from api.entity_api import EntityApi
from builders.entity_builder import EntityRequestBuilder
from config import BASE_URL


@pytest.fixture(scope="session")
def api() -> EntityApi:
    return EntityApi(BASE_URL)


@pytest.fixture
def sample_entity():
    return (
        EntityRequestBuilder()
        .title("Тестовая сущность")
        .verified(True)
        .important_numbers([1, 2, 3])
        .addition("Доп. сведения", 42)
        .build()
    )


@pytest.fixture
def created_entity_id(api, sample_entity) -> str:
    response = api.create(sample_entity)
    assert response.status_code == 200, f"Не удалось создать сущность: {response.text}"
    entity_id = response.text.strip()
    yield entity_id
    api.delete(entity_id)
