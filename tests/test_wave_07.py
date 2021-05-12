def test_get_tasks_sorted_by_id_asc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort_by_id=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {
            "id": 1,
            "title": "Water the garden 🌷",
            "description": "",
            "is_complete": False
        },
        {   "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False
        },
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False
        }
    ]
    
def test_get_tasks_sorted_by_id_desc(client, three_tasks):
    # Act
    response = client.get("/tasks?sort_by_id=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {   "description": "",
            "id": 3,
            "is_complete": False,
            "title": "Pay my outstanding tickets 😭"
        },
        {   "description": "",
            "id": 2,
            "is_complete": False,
            "title": "Answer forgotten email 📧"
        },
        {
            "description": "",
            "id": 1,
            "is_complete": False,
            "title": "Water the garden 🌷"},
    ]