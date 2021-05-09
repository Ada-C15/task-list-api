from flask import current_app
from app import db
from datetime import datetime ## IS THIS CORRECT???

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # do i set it to autoincrement?
    title = db.Column(db.String) # or title (this is the name of the task)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, nullable=True)
    #completed_at = db.Column(db.DateTime, index=False, unique=False, nullable=True)
    # adding one to many relationship  tasks to goal == >dog to person 
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True) # # nullable means task might not belong to a goal

    def to_json_response(self):
        return {"task": 
                        {"id": self.id,
                        "title": self.title,
                        "description": self.description,
                        "is_complete": bool(self.completed_at)}
                } 
    def task_to_json_response(self):
        return {"id": self.id,
                "title": self.title,
                "description": self.description,
                "is_complete": bool(self.completed_at)}

# A task's is_complete is true when there is a datetime for 
# the task's completed_at value. A task's is_complete is 
# false when there is a null/None value for the tasks's 
# completed_at value.
    def set_completion(self):   # if method is called, it changes completed_at 
                                # with currentdate/time
        complete_time = (datetime.now()).strftime("%c")
        self.completed_at = complete_time ## completed at gets updated to date/time it's right now. 


# for reference
# import datetime
# now = datetime.datetime.now()
# print(now.strftime("%A"), now) 
# ==> Friday 2021-05-07 16:26:45.456577

# OR 
# import datetime

# x = datetime.datetime.now()
# print(x.strftime("%c")) ==> Fri May 07 09:29:22 2021 

# print(x)
# print(x.strftime("%A"))
# https://www.w3schools.com/python/trypython.asp?filename=demo_datetime2
# %a 	Weekday, short version 	Wed 	
# %A 	Weekday, full version 	Wednesday
# %c 	Local version of date and time 	Mon Dec 31 17:41:00 2018

# https://stackoverflow.com/questions/15707532/import-datetime-v-s-from-datetime-import-datetime