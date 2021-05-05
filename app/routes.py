from flask import Blueprint
from app import db
from app.models.task import Task
from flask import jsonify
from flask import request, make_response


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"])
def handle_tasks():
    request_body = request.get_json()
    new_task = Task(title=request_body["title"], 
    description=request_body["description"], 
    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()
    return make_response({"task":new_task.to_json()}, 201)


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    return jsonify(tasks_response), 200 


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return {"details": "Task 1 \"Go on my daily walk 🏞\" successfully deleted"}
    #something for a 404 here

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return make_response({"task":task.to_json()}, 200)
    # and here too

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        new_data = request.get_json()
        task.title = new_data["title"]
        task.description = new_data["description"]
        task.completed_at = new_data["completed_at"]

        db.session.commit()
        return make_response({"task":task.to_json()}, 200)
    #TODO: return 404 here