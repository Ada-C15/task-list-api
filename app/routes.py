from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify

task_list_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# make a post request

@task_list_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"]

    db.session.add(new_add)
    db.session.commit() 

    return make_response({
        "task":{
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at
        }}), 201