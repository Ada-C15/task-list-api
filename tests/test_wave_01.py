def test_index(client):
    # Act
    response = client.get("/")
    response_body = response.get_json()

    # Assert
    assert "name" in response_body
    assert "message" in response_body


def test_get_tasks_no_saved_tasks(client):
    # Act
    response = client.get("/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_tasks_one_saved_tasks(client, one_task):
    # Act
    response = client.get("/tasks")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    ]


def test_get_task(client, one_task):
    # Act
    response = client.get("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    }


def test_get_task_not_found(client):
    # Act
    response = client.get("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == None


def test_create_task_with_none_completed_at(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task",
        "description": "Test Description",
        "completed_at": None
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "A Brand New Task",
            "description": "Test Description",
            "is_complete": False
        }
    }


def test_update_task(client, one_task):
    # Act
    response = client.put("/tasks/1", json={
        "title": "Updated Task Title",
        "description": "Updated Test Description",
        "completed_at": None
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "task" in response_body
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Updated Task Title",
            "description": "Updated Test Description",
            "is_complete": False
        }
    }


def test_update_task_not_found(client):
    # Act
    response = client.put("/tasks/1", json={
        "title": "Updated Task Title",
        "description": "Updated Test Description",
        "completed_at": None
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == None


def test_delete_task(client, one_task):
    # Act
    response = client.delete("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "details" in response_body
    assert response_body == {
        "details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'
    }

    # Make another request to
    # check that the task was deleted
    response = client.get("/tasks/1")
    assert response.status_code == 404


def test_delete_task_not_found(client):
    # Act
    response = client.delete("/tasks/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == None


def test_create_task_must_contain_title(client):
    # Act
    response = client.post("/tasks", json={
        "description": "Test Description",
        "completed_at": None
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }


def test_create_task_must_contain_description(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task",
        "completed_at": None
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }


def test_create_task_must_contain_completed_at(client):
    # Act
    response = client.post("/tasks", json={
        "title": "A Brand New Task",
        "description": "Test Description"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert "details" in response_body
    assert response_body == {
        "details": "Invalid data"
    }
