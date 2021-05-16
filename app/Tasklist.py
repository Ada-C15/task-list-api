import requests 
import datetime

class TaskList:
    def __init__(self, url="http://localhost:5000", selected_task=None):
        self.url = url 
        self.selected_task = selected_task

    def create_task(self, title="Default Task", description="Default Description", completed_at=None):
        query_params = { "title": title ,
                        "description": description, 
                        "completed_at": completed_at 
                        }
        response = requests.post(self.url+"/tasks", json=query_params)
        return response.json()

    def create_goal(self, title="Default Goal"):
        query_params = {"title": title}

        response = requests.post(self.url+"/goals", json=query_params)
        return response.json()

    def list_tasks(self):
        response = requests.get(self.url+"/tasks")
        return response.json()

    def list_goals(self):
        response = requests.get(self.url+"/goals")
        return response.json()

    def get_task(self, title=None, id=None):
        for task in self.list_tasks():
            if title:
                if task["title"] == title:
                    id = task["id"]
                    self.selected_task = task
            elif id == task["id"]:
                self.selected_task = task
        if self.selected_task == None:
            return "Could not find a task with that name or ID. "
        
        response = requests.get(self.url+f"/tasks/{id}")
        return response.json()

    def get_goal(self, title=None, id=None):
        for goal in self.list_goals():
            if title:
                if goal["title"] == title:
                    id = goal["id"]
                    self.selected_goal = goal
            elif id == goal["id"]:
                self.selected_goal = goal
        if self.selected_goal == None:
            return "Could not find a goal with that name or ID. "

    def update_task(self, title=None, description=None, completed_at=None):
        if not title:
            title = self.selected_task["title"]
        if not description:
            description = self.selected_task["description"]

        query_params = {
                    "title": title, 
                    "description": description, 
                    "completed_at": self.selected_task["is_complete"]
        }
        response = requests.put(self.url+f"/tasks/{self.selected_task['id']}", json=query_params)
        print("response:", response)
        self.selected_task = response.json()["task"]
        return response.json()

    def update_goal(self, title=None):
        title = self.selected_goal["title"]


        query_params = {
                    "title": title

        }
        response = requests.put(self.url+f"/goals/{self.selected_goal['id']}", json=query_params)
        self.selected_goal = response.json()["goal"]
        return response.json()

    def delete_task(self):
        response = requests.delete(self.url+f"/tasks/{self.selected_task['id']}")
        self.selected_task = None 
        return response.json()

    def delete_goal(self):
        response = requests.delete(self.url+f"/goals/{self.selected_goal['id']}")
        self.selected_goal = None
        return response.json()

    def mark_complete(self):
        response = requests.patch(self.url+f"/tasks/{self.selected_task['id']}/mark_complete")
        self.selected_task = response.json()["task"]
        return response.json()

    def mark_incomplete(self):
        response = requests.patch(self.url+f"/tasks/{self.selected_task['id']}/mark_incomplete")
        self.selected_task = response.json()["task"]
        return response.json()

    def print_selected(self):
        if self.selected_task:
            print(f"Task with id {self.selected_task['id']} is currently selected\n")

