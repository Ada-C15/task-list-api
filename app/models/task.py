from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    completed_at = db.Column(db.DateTime)
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.goal_id'), nullable=True)

    def task_to_json(self):
        to_json = {
            "id": self.id,
            "title": self.title,
            "description":self.description,
            "is_complete": bool(self.completed_at)
        }
        if self.goal_id:
            to_json["goal_id"] = self.goal_id
            return to_json
        return to_json