from flask import request, Blueprint, make_response
from app import db
from .models.task import Task
from flask import jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    try:  
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])
    except KeyError:
        return jsonify({"details": "Invalid data"}), 400
    # print(new_task.title)
    # if not new_task.title:
    #     return jsonify({"details": "Invalid data"}), 400
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_json()}), 201


@tasks_bp.route("", methods=["GET"])
def get_task():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET"])
def get_single_task(task_id):
    # if not int(task_id):
    #     return make_response("", 404)
    
    task = Task.query.get(task_id)

    if task:
        return jsonify({"task": task.to_json()}), 200

    return make_response("", 404)

@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task": task.to_json()}), 200

@tasks_bp.route("<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "details": f'Task {task_id} \"Go on my daily walk 🏞\" successfully deleted'
    })


