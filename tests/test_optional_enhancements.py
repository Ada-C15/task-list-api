def test_get_tasks_sorted_by_id(client, three_tasks):
    # Act
    response = client.get("/tasks?sort_by_id=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "description": "",
            "id": 1,
            "is_complete": False,
            "title": "Water the garden 🌷"},
        {
            "description": "",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧"},
        {
            "description": "",
            "id": 3,
            "is_complete": False,
            "title": "Pay my outstanding tickets 😭"}
    ]

def test_get_tasks_sorted_by_id_desc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort_by_id=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "description": "",
            "id": 3,
            "is_complete": False,
            "title": "Pay my outstanding tickets 😭"},
        {
            "description": "",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧"},
        {
            "description": "",
            "id": 1,
            "is_complete": False,
            "title": "Water the garden 🌷"}
    ]

def test_get_tasks_filtered_by_title(client, three_tasks):
    # Act
    response = client.get("/tasks?filter_by_title=Answer%20forgotten%20email%20📧")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "description": "",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧"}
    ]

def test_get_goals_sorted_asc(client, three_goals):
    # Act
    response = client.get("/goals?sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 2,
            "title": "Go solo paragliding"
        },
        {
            "id": 1,
            "title": "Run an ultramarathon"
        },
        {
            "id": 3,
            "title": "Save a million dollars"
        }
    ]


def test_get_goals_sorted_desc(client, three_goals):
    # Act
    response = client.get("/goals?sort=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 3,
            "title": "Save a million dollars"
        },
        {
            "id": 1,
            "title": "Run an ultramarathon"
        },
        {
            "id": 2,
            "title": "Go solo paragliding"
        }
    ]

def test_get_goals_sorted_by_id(client, three_goals):
    # Act
    response = client.get("/goals?sort_by_id=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 1,
            "title": "Run an ultramarathon"
        },
        {
            "id": 2,
            "title": "Go solo paragliding"
        },
        {
            "id": 3,
            "title": "Save a million dollars"
        }
    ]

def test_get_goals_sorted_by_id_desc(client, three_goals):
    # Act
    response = client.get("/goals?sort_by_id=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 3,
            "title": "Save a million dollars"
        },
        {
            "id": 2,
            "title": "Go solo paragliding"
        },
        {
            "id": 1,
            "title": "Run an ultramarathon"
        }
    ]

def test_get_goals_filtered_by_title(client, three_goals):
    # Act
    response = client.get("/goals?filter_by_title=Go%20solo%20paragliding")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {
            "id": 2,
            "title": "Go solo paragliding"
        }
    ]