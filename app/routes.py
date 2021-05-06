from flask import request, Blueprint, make_response
from app import db
from flask import jsonify
from .models.task import Task

task_bp = Blueprint("task", __name__, url_prefix="/tasks")





@task_bp.route("", methods=["POST"], strict_slashes=False)
def add_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        
        "task":{
            "id": f"{new_task.task_id}",
            "title": f"{new_task.title}",
            "description": f"{new_task.description}",
            "is_complete": f"{new_task.convert_complete()}"
        }
    }), 201

@task_bp.route("", methods=["GET"], strict_slashes=False)
def task_index():
    tasks = Task.query.all()
    task_response = []
    for task in tasks:
        task_response.append(task.to_json())
    return jsonify(task_response), 200
    