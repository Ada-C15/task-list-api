from flask import request,Blueprint,make_response,jsonify

from app import db
from app.models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def handle_tasks():
    
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=null)

    db.session.add(new_task)
    db.session.commit()

    return  jsonify(new_task),201