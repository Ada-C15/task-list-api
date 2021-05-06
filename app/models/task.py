from app import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)

    # helper function to convert "complete" to true or false
    def complete_helper(self):
        if self.completed_at == None: # if empty return false, if not empty return true
            complete = False
        else:
            complete = True
        return complete
    


    
    
