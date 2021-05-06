from app import db
from flask import request, Blueprint, make_response, jsonify
from app.models.task import Task


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods = ["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        tasks = Task.query.all()
        tasks_response = []
        for task in tasks:
            task_response.append({
                "id" : task.id,
                "title" : task.title,
                "description" : task.description,
                "completed at" : task.completed_at
            })
        return jsonify(tasks_response)
    elif request.method == "POST":
        request_body = request.get_json()
        new_task = Task (
            title = request_body["title"],
            description = request_body["description"],
            completed_at = request_body["completed at"]
        )
        db.session.add(new_task)
        db.session.commit()

        return make_response(f"{new_task.name} has successfully been added to your task list", 200)

