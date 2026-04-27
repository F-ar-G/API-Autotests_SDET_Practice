import allure

from models.responses import EntityResponse, GetAllResponse
from builders.entity_builder import EntityRequestBuilder


@allure.feature("Entity API")
@allure.story("Create")
@allure.title("Создание сущности возвращает числовой ID")
def test_create_entity(api, sample_entity):
    response = api.create(sample_entity)

    assert response.status_code == 200
    entity_id = response.text.strip()
    assert entity_id.isdigit(), f"Ожидали числовой ID, получили: '{entity_id}'"


@allure.feature("Entity API")
@allure.story("Get")
@allure.title("Получение сущности по ID возвращает корректный объект")
def test_get_entity(api, created_entity_id):
    response = api.get(created_entity_id)

    assert response.status_code == 200
    entity = EntityResponse.model_validate(response.json())
    assert entity.id == int(created_entity_id)


@allure.feature("Entity API")
@allure.story("GetAll")
@allure.title("Получение всех сущностей возвращает список")
def test_get_all_entities(api, created_entity_id):
    response = api.get_all()

    assert response.status_code == 200
    result = GetAllResponse.model_validate(response.json())
    assert isinstance(result.entity, list)
    assert len(result.entity) > 0


@allure.feature("Entity API")
@allure.story("Patch")
@allure.title("Обновление сущности возвращает 204")
def test_patch_entity(api, created_entity_id):
    updated = (
        EntityRequestBuilder()
        .title("Обновлённая сущность")
        .verified(False)
        .important_numbers([10, 20, 30])
        .addition("Новые сведения", 99)
        .build()
    )

    response = api.patch(created_entity_id, updated)

    assert response.status_code == 204


@allure.feature("Entity API")
@allure.story("Delete")
@allure.title("Удаление сущности возвращает 204")
def test_delete_entity(api, created_entity_id):
    response = api.delete(created_entity_id)

    assert response.status_code == 204


@allure.feature("Entity API")
@allure.story("GetAll")
@allure.title("Фильтрация по title возвращает только совпадающие сущности")
def test_get_all_with_title_filter(api, created_entity_id, sample_entity):
    response = api.get_all(title=sample_entity.title)

    assert response.status_code == 200
    result = GetAllResponse.model_validate(response.json())
    assert all(e.title == sample_entity.title for e in result.entity)
    assert any(e.id == int(created_entity_id) for e in result.entity)


@allure.feature("Entity API")
@allure.story("GetAll")
@allure.title("Фильтрация по verified=True возвращает только подтверждённые сущности")
def test_get_all_with_verified_filter(api, created_entity_id):
    response = api.get_all(verified=True)

    assert response.status_code == 200
    result = GetAllResponse.model_validate(response.json())
    assert len(result.entity) > 0
    assert all(e.verified is True for e in result.entity)


@allure.feature("Entity API")
@allure.story("GetAll")
@allure.title("Пагинация perPage=1 возвращает ровно один элемент")
def test_get_all_with_pagination(api, created_entity_id):
    response = api.get_all(page=1, perPage=1)

    assert response.status_code == 200
    result = GetAllResponse.model_validate(response.json())
    assert len(result.entity) == 1
