from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def is_complete_function(completed_at):
        if completed_at is not None:
            return True
        else:
            return False

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def handle_tasks():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return jsonify({"details": "Invalid data"}), 400
    
    new_task = Task(title= request_body["title"],
    description= request_body["description"],
    completed_at= request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": {
        "id": new_task.task_id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": is_complete_function(new_task.completed_at)}}), 201


@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def tasks_index():
    tasks = Task.query.all()
    tasks_response = []
    
    if tasks is None:
        return jsonify(tasks_response), 200
    
    else:
        for task in tasks:
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": is_complete_function(task.completed_at)
            })
        return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def handle_single_task(task_id):

    task = Task.query.get(task_id)

    if task is None:
            return jsonify(None), 404
    
    return jsonify({"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete_function(task.completed_at)}}), 200
    

@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_single_task(task_id):
    task = Task.query.get(task_id)

    request_body = request.get_json()

    if task is None:
            return jsonify(None), 404
    
    # elif "title" not in request_body or "description" not in request_body:
    #     return {"message": "Request requires both a title and description."}, 400

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]

    db.session.commit()

    return jsonify({"task": {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "is_complete": is_complete_function(task.completed_at)}}), 200


@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
            return jsonify(None), 404
    
    db.session.delete(task)
    db.session.commit()

    return jsonify({"details" : f"Task {task.task_id} \"{task.title}\" successfully deleted"}), 200

