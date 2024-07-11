from datetime import datetime

import pytest

from response_models import ResourceRequestResponse, ResourceRequest
from request_models import ProjectTaskRequestBody


def test_get_resource_requests_by_project_by_project(client):
    response = client.get_projects_resource_requests_by_project()
    assert response.status_code == 200
    ResourceRequestResponse(project_tasks=response.json())

def test_get_projects_resource_requests_by_company(client):
    response = client.get_projects_resource_requests_by_company()
    print(response.json())
    assert response.status_code == 200
    ResourceRequestResponse(project_tasks=response.json())


@pytest.mark.parametrize("is_over_budget", [False, True], indirect=True, ids=['isn`t over budget',
                                                                              'is over budget'])
@pytest.mark.parametrize("volume", ["5", 5, "b"], ids=["string number", "int", "string letter"])
def test_post_resource_requests(client, resource, is_over_budget, volume):
    data = ProjectTaskRequestBody(
        project_tasks_resource_id=resource,
        volume=volume,
        cost="5",
        is_over_budget=is_over_budget,
        needed_at=int(datetime.now().timestamp()),
    )

    response = client.post_projects_resource_requests(data=data)

    if is_over_budget == 1 and volume != 'b':
        assert response.status_code == 201
    elif is_over_budget == 0 or volume != 'b':
        assert response.status_code == 422

9498614
@pytest.mark.parametrize("test_resource", [0, 9498614, 'b24dwwd', 99992222], ids=['valid_id', 'other_proj_id',
                                                                                 'string_id', 'not_existing_id'])
def test_get_projects_resource_request(client, resource_request, test_resource):
    if test_resource != 0:
        resource_request = test_resource
    response = client.get_projects_resource_request(resource_request)
    print(response.json())

    print(len(str(test_resource)))
    if type(test_resource) == int and len(str(test_resource)) == 7:
        assert response.status_code == 200
    elif not isinstance(test_resource, int):
        assert response.status_code == 404
    elif len(str(test_resource)) > 7:
        assert response.status_code == 404

@pytest.mark.parametrize("is_over_budget", [False, True], indirect=True, ids=['isn`t over budget',
                                                                              'is over budget'])
@pytest.mark.parametrize("needed_at", [0, '10.07.24', int(datetime.now().timestamp())], ids=['unchanged needed_at',
                                                                              'string needed_at',
                                                                                             'datetime needed_at'])
@pytest.mark.parametrize("volume", ["5", 0], ids=["string number volume", "not editing volume"])

def test_edit_projects_resource_request(client, resource_request, is_over_budget, needed_at, volume):
    pre_edit_resource_request = client.get_projects_resource_request(resource_request)
    pre_edit_rq_data = pre_edit_resource_request.json()

    if needed_at == 0:
        needed_at = pre_edit_rq_data['needed_at']

    data = {
        "is_over_budget": is_over_budget,
        "needed_at": needed_at,
    }

    if volume != 0:
        data["volume"] = volume
    response = client.edit_projects_resource_request(resource_request, data=data)
    print(response.json())

    if not isinstance(needed_at, int):
        assert response.status_code == 422
    elif is_over_budget is False and volume == "5":
        assert response.status_code != 200
    else:
        assert response.status_code == 200

@pytest.mark.parametrize("test_resource", [0, 'b24dwwd'], ids=['valid_id', 'string_id'])
@pytest.mark.parametrize("is_over_budget", [False, True], indirect=True, ids=['isn`t over budget',
                                                                              'is over budget'])
def test_delete_projects_resource_request(client, resource, is_over_budget, test_resource):
    data = ProjectTaskRequestBody(
        project_tasks_resource_id=resource,
        volume="5",
        cost="5",
        is_over_budget=is_over_budget,
        needed_at=int(datetime.now().timestamp()),
    )


    request_id = client.post_projects_resource_requests(data=data).json()["id"]

    if test_resource != 0:
        request_id = test_resource

    response = client.delete_projects_resource_request(request_id)
    if is_over_budget == 1 and request_id != 'b24dwwd':
        assert response.status_code == 204
    elif is_over_budget == 0 and request_id != 'b24dwwd':
        assert response.status_code == 422
    elif request_id == 'b24dwwd':
        assert response.status_code == 404




