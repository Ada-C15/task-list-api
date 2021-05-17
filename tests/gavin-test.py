import requests

task = {
                "title": "laundry",
                "description": "wash laundry",
            }

response = requests.post(url="http://localhost:5000/tasks:", data=task)
print(f"code:{response}, text:{response.text}")
