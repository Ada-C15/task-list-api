from flask import Blueprint
from .models.task import Task
from flask import request


tasks_bp = Blueprint("task", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])

def create_tasks():
    request_body = request.get_json()

    new_task = Task(title = request_body["title"],
                description = request_body["description"])

    db.session.add(new_task)
    db.session.commit()
    
    return {
        "task": new_task.to_json()
        }, 201
