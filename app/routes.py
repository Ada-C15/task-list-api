from flask import Blueprint, request, make_response, jsonify
from app.models.task import Task
from app import db

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST", "GET"])
def handle_tasks():
    if request.method == "GET":
        tasks = Task.query.all()

        tasks_response = []
        for task in tasks:
            tasks_response.append({
                "task_id": task.task_id,
                "title": task.title,
                "description": task.description,
                "completed_at": task.completed_at
            })
        return jsonify(tasks_response)

    elif request.method == "POST":
        request_body = request.get_json()
        new_task = Task(title=request_body["title"],
        description=request_body["description"],
        completed_at=request_body["completed_at"])

        db.session.add(new_task)
        db.session.commit()

        return make_response(f"Task {new_task.title} successfully created", 201)
