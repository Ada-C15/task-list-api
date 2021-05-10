from flask import current_app
from app import db

class Task(db.Model):
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    #WAVE 3
    is_complete = False

    #WAVE 6
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True) #wave 6
    
    
    def compute_is_complete(self):
        if self.completed_at == None:
            return False
        else:
            return True #wave 3
    
    #Create an instance method in Task named to_json()
    def to_json(self):
        return {
                "task":     
                       {
                            "id": self.task_id,
                            "title": self.title,
                            "description": self.description,
                            "is_complete": self.compute_is_complete()
                        }
                     }
        
    def to_json_no_key(self):    
                return {
                            "id": self.task_id,
                            "title": self.title,
                            "description": self.description,
                            "is_complete": self.compute_is_complete()
                        }
    
    
    # #WAVE 6 includes goal_id
    def to_json_with_goal_id(self): 
        return {
                            "id": self.task_id,
                            "goal_id": self.goal_id,
                            "title": self.title,
                            "description": self.description,
                            "is_complete": self.compute_is_complete()
                        }
    
    
    #WAVE 6 includes goal_id and task key
    def to_json_with_goalid_and_key(self):  
        return {
                "task":     
                       {
                            "id": self.task_id,
                            "goal_id": self.goal_id,
                            "title": self.title,
                            "description": self.description,
                            "is_complete": self.compute_is_complete()
                        }
                     }
     
    #optional enhancement Create a class method in Task named from_json(): Converts JSON into a new instance of Task
    @staticmethod
    def from_json(task_json):
        
        task_goal_id = None
        if ("goal_id" in task_json):
            task_goal_id = task_json["goal_id"]
        
        return Task(title=task_json["title"],
                    description=task_json["description"],
                    completed_at=task_json["completed_at"],
                    goal_id = task_goal_id)
        
        
    #did not use this function                  
    def to_string(self):
        return f"{self.task_id}: {self.title} Description: {self.description} completed at {self.completed_at} " 
        
    