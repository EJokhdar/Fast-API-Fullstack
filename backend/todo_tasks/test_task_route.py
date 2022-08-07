import pytest
from datetime import datetime
from my_enums import Status


def test_created_task(client):

    before_create = client.get(
        "/tasks"
    )
    before_create_length = len(before_create.json())

    empty_request = client.post(
        "/tasks",
        json={}
    )
    assert empty_request.status_code == 422, empty_request.text

    full_request = client.post(
        "/tasks",
        json={"task_name": "test code"}
    )
    assert full_request.status_code == 201, full_request.text

    after_create = client.get(
        "/tasks"
    )
    after_create_length = len(after_create.json())

    assert after_create_length == before_create_length+1

    task = full_request.json()
    task_id = task["task_id"]
    task_name = task["task_name"]
    task_checked = task["checked"]
    task_status = task["task_status"]
    expire_at = task["expire_at"]
    
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200, response.text
    assert response.json()["task_id"] == task_id
    assert response.json()["task_name"] == task_name
    assert response.json()["checked"] == task_checked
    assert response.json()["task_status"] == task_status
    assert response.json()["expire_at"] == expire_at
    
    '''TEARDWON FOR TEST'''
    delete_task = client.delete(f"/tasks/{task_id}")
    
    get_deleted = client.get(f"/tasks/{task_id}")
    
    assert get_deleted.status_code == 404, get_deleted.text


def test_get_all_task(client):
    request = client.get(
        f"/tasks"
    )
    assert request.status_code == 200, request.text

    request_length = len(request.json())

    new_task = client.post(
        "/tasks",
        json={"task_name": "sample"}
    )
    data = new_task.json()
    task_id = data["task_id"]

    assert new_task.status_code == 201, new_task.text

    get_length = client.get(
        f"/tasks"
    )

    new_length = len(get_length.json())

    assert request_length+1 == new_length

    data = new_task.json()
    task_id = data["task_id"]
    delete_new_task = client.delete(
        f"/tasks/{task_id}"
    )
    assert delete_new_task.status_code == 200, delete_new_task.text

    check_if_deleted = client.get(
        f"/tasks/{task_id}"
    )

    assert check_if_deleted.status_code == 404, check_if_deleted.text


def test_get_task(client, redis, create_delete_task):
    task = create_delete_task.json()
    task_id = task["task_id"]

    get_task = client.get(
        f"/tasks/{task_id}"
    )

    assert get_task.status_code == 200, get_task.text


def test_delete_task(client, redis, create_delete_task):
    task = create_delete_task.json()
    task_id = task["task_id"]

    before_delete = client.get(
        "/tasks"
    )
    before_delete_length = len(before_delete.json())

    response = client.delete(
        f"/tasks/{task_id}"
    )
    assert response.status_code == 200, response.text
    after_delete = client.get(
        "/tasks"
    )
    after_delete_length = len(after_delete.json())

    assert after_delete_length+1 == before_delete_length

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404, response.text


def test_toggle_task(client, redis, create_delete_task):
    task = create_delete_task.json()
    task_id = task["task_id"]
    task_checked = task["checked"]

    request = client.post(
        f"/tasks/{task_id}/toggle"
    )
    assert request.status_code == 200, request.text
    data = request.json()

    assert task_checked != data["checked"]

    request_double_toggle = client.post(
        f"/tasks/{task_id}/toggle"
    )
    assert request_double_toggle.status_code == 200, request_double_toggle.text
    data_request = request_double_toggle.json()

    assert data_request["checked"] != data["checked"]


def test_update_task(client, redis, create_delete_task):
    task = create_delete_task.json()
    task_id = task["task_id"]

    empty_request = client.put(
        f"/tasks/{task_id}",
        json={}
    )
    assert empty_request.status_code == 422, empty_request.text

    full_request = client.put(
        f"/tasks/{task_id}",
        json={"task_name": "string"}
    )
    assert full_request.status_code == 200, full_request.text
    