from datetime import datetime

import pytest

from request_models import ProjectTaskRequestBody
from tests.gectaro_http_client import GectaroHttpClient


def pytest_addoption(parser):
    parser.addoption("--token", help="token for test API")
    parser.addoption(
        "--url", default="https://api.gectaro.com", help="base url for API client"
    )


@pytest.fixture(scope="session")
def token(request):
    return request.config.getoption("--token")


@pytest.fixture(scope="session")
def url(request):
    return request.config.getoption("--url")


@pytest.fixture
def client(token, url):
    client = GectaroHttpClient(base_url=url, token=token)
    yield client
    # teardown


@pytest.fixture
def resource(client):
    data = {
        "name": "first_resource",
        "needed_at": int(datetime.now().timestamp()),
        "project_id": 80024,
        "type": 1,
        "volume": 5,
    }

    resource_id = client.post_projects_resources(data=data).json()["id"]

    print(f"resource_id: {resource_id}")
    yield resource_id

    client.delete_projects_resources(resource_id)


    # todo: delete resource

@pytest.fixture
                                                # 'negative str volume', 'negative volume'])
def resource_request(client, request, resource):
    data = ProjectTaskRequestBody(
        project_tasks_resource_id=resource,
        volume="5",
        cost="5",
        is_over_budget=True,
        needed_at=int(datetime.now().timestamp()),
    )

    request_id = client.post_projects_resource_requests(data=data).json()["id"]
    print(f"request_id: {request_id}")
    yield request_id





@pytest.fixture
def is_over_budget(request):
    return int(request.param)


