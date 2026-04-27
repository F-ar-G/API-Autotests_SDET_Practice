import allure
import requests
from typing import Callable

from models.requests import EntityRequest


class EntityApi:
    def __init__(self, base_url: str):
        self._base_url = base_url

    def _execute(self, func: Callable[[], requests.Response]) -> requests.Response:
        try:
            return func()
        except requests.exceptions.ConnectionError:
            raise RuntimeError(f"Сервер недоступен: {self._base_url}")
        except requests.exceptions.Timeout:
            raise RuntimeError(f"Превышено время ожидания ответа: {self._base_url}")

    @allure.step("POST /api/create")
    def create(self, entity: EntityRequest) -> requests.Response:
        return self._execute(lambda: requests.post(
            f"{self._base_url}/api/create",
            json=entity.model_dump(),
        ))

    @allure.step("GET /api/get/{entity_id}")
    def get(self, entity_id: str) -> requests.Response:
        return self._execute(lambda: requests.get(
            f"{self._base_url}/api/get/{entity_id}",
        ))

    @allure.step("GET /api/getAll")
    def get_all(self, **params) -> requests.Response:
        return self._execute(lambda: requests.get(
            f"{self._base_url}/api/getAll",
            params=params,
        ))

    @allure.step("PATCH /api/patch/{entity_id}")
    def patch(self, entity_id: str, entity: EntityRequest) -> requests.Response:
        return self._execute(lambda: requests.patch(
            f"{self._base_url}/api/patch/{entity_id}",
            json=entity.model_dump(),
        ))

    @allure.step("DELETE /api/delete/{entity_id}")
    def delete(self, entity_id: str) -> requests.Response:
        return self._execute(lambda: requests.delete(
            f"{self._base_url}/api/delete/{entity_id}",
        ))
