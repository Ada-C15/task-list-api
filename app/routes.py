from flask import request,Blueprint,make_response,jsonify

from app import db
from app.models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def handle_tasks():
    
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])

    db.session.add(new_task) #adding data to db(a record/row) i.e git add
    db.session.commit() # pushing it into the db i.e git commit + push
    #we need to verify that the new data is in the db
    get_task = Task.query.get(new_task.task_id) #brings data back
    return  {
        "task": {
            "id": get_task.task_id,
            "title": get_task.title,
            "description":get_task.description,
            "is_complete": get_task.is_complete()
        }
    }, 201

    