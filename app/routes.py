from app import db
from app.models.task import Task
from flask import request
from flask import request, Blueprint, task_response
from flask import jsonify

task_bp = Blueprint("task", __name__, url_prefix="/task")

@task_bp.route("", methods=["POST", "GET"], strict_slashes=False)
def task():
    if request.method == "GET":
        task = Task.query.all()
        task_response = []
        for task in task:
            task_response.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed_at": task.completed_at
            })
        return jsonify(task_response), 200

    elif request.method == "POST":
        request_body = request.get_json()
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["null"])

        db.session.add(new_task)
        db.session.commit()

        return {
            "success" : True,
            "message" : f"Task {new_task.name} has been created! wohoo!",
            }, 201