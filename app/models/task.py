from flask import current_app
from app import db
# import datetime # IS THIS CORRECT???

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # do i set it to autoincrement?
    title = db.Column(db.String) # or title (this is the name of the task)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime, index=False, unique=False, nullable=True)

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
#Requirements
    def set_completion(self):
        complete_time = (datetime.datetime.now()).strftime("%c")
        
        ## if task is not null, you can mark it as completed with date/time
        self.completed_at = complete_time ## completed at gets updated to this new date
        ## don't need this (below) because it's already null which is none and in boolean language is False
        ## self.completed_at = None

        # if mark_complete is true
        # turn completed_at to the the date it's right now. 
    

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