from app import db
from flask import Blueprint
from flask import request
from flask import jsonify
from .models.task import Task


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def tasks():
    request_body = request.get_json()
    new_task = Task(title = request_body["title"],
                        description = request_body["description"]
                        completed_at = null)
    
    db.session.add(new_task)
    db.session.commit()

    return {"task": {
    "id": 1,
    "title": "A Brand New Task",
    "description": "Test Description",
    "is_complete": false}
    }, 201

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_saved_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json() )
    
    return jsonify(tasks_response), 200

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_no_saved_tasks():
    tasks = Task.query.all()
    if tasks == []:
        return jsonify(tasks), 200

@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_single_task(task_id):

    if not is_int(task_id):
        return {
            "message": f"ID {task_id} must be an integer",
            "success": False
        }, 400

    task = Task.query.get(task_id)

    if task:
        return task.to_json(), 200
    
    return {
        "message": f"Task with id {task_id} was not found",
        "success": False,
    }, 404

@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    task = Task.query.get(task_id)
    
    if task == None:
        return Response("", status=404)
    
    if task: 
        form_data = request.get_json()

        task.name = form_data["name"]
        task.description = form_data["description"]

        db.session.commit()

        return Response(f"Task #{task.id} successfully updated", status=200)

@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)    
def delete_single_task(task_id):
    task = Task.query.get(task_id)

    if task == None:
        return Response("", status=404)

    if task:
        db.session.delete(task)
        db.session.commit()

        return Response(f"Task #{task.id} successfully deleted", status=200)
