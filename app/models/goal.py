from flask import current_app
from app import db


class Goal(db.Model):
    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False) #add nullable=False ?? what is this?
    # Establishing one to many relationships to Task Model by adding
    # tasks ==>  like person to dogs
    tasks = db.relationship('Task', backref="goal", lazy=True)
    
    def goal_to_json_response(self):
        return {"goal": 
                        {"id": self.goal_id,
                        "title": self.title}}

    def simple_response(self):
        return {"id": self.goal_id,
                "title": self.title}

    # def one_goal_tasks_response(self, goal_id, title, tasks.task_id, tasks.title, tasks.description, tasks.completed_at):
    # def one_goal_with_tasks_response(self):
    #     tasks_list =
    #     return {"id": self.goal_id,
    #             "title": self.title,
    #             "tasks": self.tasks.task_to_json_response}
    #     # CONNECT WITH 
    #                 [{ "id": tasks.id,
    #                     "goal_id": self.goal_id,
    #                     "title": tasks.title,
    #                     "description": tasks.description,
    #                     "is_complete": bool(tasks.completed_at)}]
    #     pass

# IT SHOULD LOOK LIKE THIS
    # {
    # "id": 333,
    # "title": "Build a habit of going outside daily",
    # "tasks": [
    #     {
    #     "id": 999,
    #     "goal_id": 333,
    #     "title": "Go on my daily walk 🏞",
    #     "description": "Notice something new every day",
    #     "is_complete": false
    #     }
    # ]
    # }
    

