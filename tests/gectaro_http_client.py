import logging
from typing import Union

import requests

from request_models import ProjectTaskRequestBody


class GectaroHttpClient:

    def __init__(self, base_url, token, project_id="80024", companies="7323"):
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {token}"
        self.base_url = base_url
        self.project_id = project_id
        self.companies = companies

    def get_projects_resource_requests_by_project(self):
        """Получить список заявок по проекту"""
        response = self.session.get(
            f"{self.base_url}/v1/projects/" f"{self.project_id}/resource-requests"
        )
        return response

    def get_projects_resource_requests_by_company(self):
        response = self.session.get(
            f"{self.base_url}/v1/companies/" f"{self.companies}/resource-requests"
        )
        return response

    def post_projects_resources(self, data: dict):
        response = self.session.post(
            f"{self.base_url}/v1/projects/" f"{self.project_id}/resources", json=data
        )
        return response

    def delete_projects_resources(self, resource_id):
        response = self.session.delete(
            f"{self.base_url}/v1/projects/" f"{self.project_id}/resources/" f"{resource_id}"
        )
        # logging.info(response.json())
        return response

    def post_projects_resource_requests(
        self, data: Union[dict, ProjectTaskRequestBody]
    ):
        # data может быть либо dict, либо моделью ProjectTaskRequestBody
        response = self.session.post(
            f"{self.base_url}/v1/projects/" f"{self.project_id}/resource-requests",
            # если data - это dict, не меняем,
            # а если модель - то конвертируем в словарь
            # с помощью .model_dump()
            json=data if isinstance(data, dict) else data.model_dump(),
        )
        return response

    def get_projects_resource_request(self, resource_request):
        """Получить данные заявки"""
        response = self.session.get(
            f"{self.base_url}/v1/projects/" f"{self.project_id}/resource-requests/" f"{resource_request}"
        )
        return response

    def edit_projects_resource_request(self, resource_request, data: dict):
        response = self.session.put(
            f"{self.base_url}/v1/projects/" f"{self.project_id}/resource-requests/" f"{resource_request}",
            json=data
        )
        return response

    def delete_projects_resource_request(self, resource_request):
        response = self.session.delete(
            f"{self.base_url}/v1/projects/" f"{self.project_id}/resource-requests/" f"{resource_request}"
        )
        return response

