def test_filter_tasks_by_title(client,three_tasks): 
    #Act 
    response = client.get("/tasks?filter=Answer forgotten email 📧")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [{
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False,
        }]


def test_sort_tasks_by_id(client,three_tasks): 
    #Act 
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
            "is_complete": False,},

        {
            "id": 2,
            "title": "Answer forgotten email 📧",
            "description": "",
            "is_complete": False,},
        {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",
            "description": "",
            "is_complete": False},
       
    ]

def test_sort_goals_by_title(client,three_goals): 
    #Act 
    response = client.get("/goals?sort=title")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 3
    assert response_body == [
         {
            "id": 2,
            "title": "Answer forgotten email 📧",},
         {
            "id": 3,
            "title": "Pay my outstanding tickets 😭",},
       
        {
            "id": 1,
            "title": "Water the garden 🌷",},

        
    ]


 
