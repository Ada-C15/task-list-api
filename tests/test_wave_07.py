import pytest
from app import create_app
from app.models.goal import Goal
from app import db

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
    
def test_get_tasks_filter_by_title(client, three_tasks):
    # Act
    response = client.get("/tasks?filter_by_title=Pay my outstanding tickets 😭")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {   "description": "",
            "id": 3,
            "is_complete": False,
            "title": "Pay my outstanding tickets 😭"
        }
    ]
    
def test_get_goals_sort_by_title_asc(client, three_goals):
    # Act
    response = client.get("/goals?sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
       {
            "id": 2,
            "title": "Become expert in one field",
       },
       {
            "id": 1,
            "title": "Find a new job",
       },
      {
            "id": 3,
            "title": "Keep healthy schedule",
      }
    ]
    
def test_get_goals_sort_by_title_desc(client, three_goals):
    # Act
    response = client.get("/goals?sort=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
       {
            "id": 3,
            "title": "Keep healthy schedule",
       },
       {
            "id": 1,
            "title": "Find a new job",
       },
      {
            "id": 2,
            "title": "Become expert in one field",
      }
    ]
    
@pytest.fixture   
def three_goals(app):
    db.session.add_all([
    Goal(
        title="Find a new job"),
    Goal(
        title="Become expert in one field"),
    Goal(
        title="Keep healthy schedule")
])
    db.session.commit()