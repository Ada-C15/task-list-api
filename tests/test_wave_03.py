import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from app.models.task import Task


def test_toggle_complete_on_incomplete_task(client, one_task):
    # Arrange
    """
    The future Wave 4 adds special functionality to this route,
    so for this test, we need to set-up "mocking."

    Mocking will help our tests work in isolation, which is a
    good thing!

    We need to mock any POST requests that may occur during this
    test (due to Wave 4).

    There is no action needed here, the tests should work as-is.
    """
    with patch("app.routes.requests.post") as mock_get:
        mock_get.return_value.status_code = 200

        # Act
        response = client.patch("/tasks/1/complete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert "task" in response_body
    assert response_body["task"]["is_complete"] == True
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": True
        }
    }
    assert Task.query.get(1).completed_at


def test_toggle_complete_on_complete_task(client, completed_task):
    # Act
    response = client.patch("/tasks/1/complete")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["task"]["is_complete"] == False
    assert response_body == {
        "task": {
            "id": 1,
            "title": "Go on my daily walk 🏞",
            "description": "Notice something new every day",
            "is_complete": False
        }
    }
