#test to get tasks sorted by id
def test_get_tasks_sorted_by_id(client, three_tasks):
    # Act
    response = client.get("/tasks?sort=id")
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
    

#Tests for goals sorted by title asc/desc
def test_get_goals_sorted_asc(client, three_goals):
    # Act
    response = client.get("/goals?sort=asc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {   
            "id" : 2,
            "title": "Eat healthy"},
        {   "id" : 3, 
            "title": "Get better sleep"}, 
        {   
            "id" : 1,
            "title": "Get more excercise"}
    ]


#Test for getting a response body with goals sorted by title
def test_get_goals_sorted_desc(client, three_goals):
    # Act
    response = client.get("/goals?sort=desc")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
        {   
            "id" : 1,
            "title": "Get more excercise"}, 
        {   "id" : 3, 
            "title": "Get better sleep"},
        {   
            "id" : 2,
            "title": "Eat healthy"} 
    ]

