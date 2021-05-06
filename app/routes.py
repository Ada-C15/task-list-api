from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")
goals_bp = Blueprint("goals", __name__, url_prefix="/goals")


@tasks_bp.route("", methods=["GET", "POST"])
def handle_tasks():
    if request.method == "GET":
        tasks = Task.query.all()
        tasks_response = []
        for task in tasks:
            tasks_response.append({
                "task_id" : task.task_id,
                "description" : task.description,
                "is_complete": 'false'
            })
        return jsonify(tasks_response)
    
    elif request.method == "POST":

        request_body = request.get_json()
        new_task = Task(
            title = request_body["title"],
            description = request_body["description"],
            completed_at = request_body["completed_at"]
        )
        db.session.add(new_task)
        db.session.commit()

        return make_response(f"Task {new_task.title} successfully created", 201)


@tasks_bp.route("/<task_id>", methods=["GET"])
def handle_task(task_id):
    task = Task.query.get(task_id)

    return {
        "task_id" : task.task_id,
        "description" : task.description,
        "is_complete": 'false'
    }