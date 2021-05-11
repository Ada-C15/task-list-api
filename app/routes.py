from flask import Blueprint, request, jsonify
from app import db
from flask.helpers import make_response
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET","POST"], strict_slashes=False)
def handle_tasks():
    if request.method == "GET":
        task_title_from_url = request.args.get("title")
        # search for task by title
        if task_title_from_url:
            tasks = Task.query.filter_by(title=task_title_from_url)
        # all tasks
        else:
            tasks = Task.query.all()
    
        tasks_response = []

        for task in tasks:
            tasks_response.append(task.to_json())

        return jsonify(tasks_response), 200

    elif request.method == "POST":
        # try and except block for KeyError
        try:
            request_body = request.get_json()

            new_task = Task(title=request_body["title"],
                            description=request_body["description"],
                            completed_at=request_body["completed_at"]
                            )

            db.session.add(new_task)
            db.session.commit()

            return {
                "task": new_task.to_json()
            }, 201
        
        except KeyError:
            return{"details": "Invalid data"}, 400