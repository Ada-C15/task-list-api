from datetime import datetime
from app.models.task import Task
from app.models.goal import Goal

def test_task_sort_by_column_name(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=id")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False},
        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False},
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False}
    ]
    
def test_task_sort_by_invalid_parameter(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=blah_blah_blah")
    response_body = response.get_json()
    # Assert
    assert response.status_code == 400
    assert response_body == {"details":"Invalid data"}

def test_update_task_missing_attributes(client, one_task):
    # Act
    response = client.put("/tasks/1", json={
        "description": "New Description",
        "completed_at": None
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }

def test_create_task_invalid_timestamp(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task",
        "description": "Test Description",
        "completed_at": "I Love Bananas!!!!"
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 400
    assert response_body == {"details": "Invalid data"}

def test_update_task_invalid_timestamp(client, one_task):
    # Act
    response = client.put("/tasks/1", json={
        "title": "A Brand New Task",
        "description": "Test Description",
        "completed_at": 1324566
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 400
    assert response_body == {"details": "Invalid data"}

def test_post_task_ids_to_goal_missing_task_ids(client, one_goal, three_tasks):
    # Act
    response = client.post("/goals/1/tasks", json={})
    response_body = response.get_json()
    # Assert
    assert response.status_code == 400
    assert response_body == {"details":"Invalid data"}
    assert len(Goal.query.get(1).tasks) == 0

def test_post_task_ids_to_goal_empty_list(client, one_goal, three_tasks):
    # Act
    response = client.post("/goals/1/tasks", json={
        "task_ids": []
    })
    response_body = response.get_json()
    # Assert
    assert response.status_code == 200
    assert "id" in response_body
    assert "task_ids" in response_body
    assert response_body == {
        "id": 1,
        "task_ids": []
    }
    assert len(Goal.query.get(1).tasks) == 0