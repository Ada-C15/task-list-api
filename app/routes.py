from flask import Blueprint
import flask_migrate
from app import db 
from app.models.task import Task 
from flask import request, Blueprint, make_response 
from flask import jsonify


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_task():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed_at": task.completed_at 
            }, 200)
    return jsonify(tasks_response)

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()
    new_task = Task(title = request_body["title"], 
                    description = request_body["description"], 
                    completed_at = request_body["completed_at"])
    db.session.add(new_task)
    db.session.commit() 

    return {
        "task": new_task.to_json()
    }, 201

def is_int(value):
    try: 
        return int(value)
    except ValueError:
        return False

@tasks_bp.route("/tasks/<task_id>", methods=["GET","PUT", "DELETE"], strict_slashes=False)
def handle_task(task_id):
    task = Task.query.get(task_id)
    
    if task is None:
        return make_response("", 404)
    
    if not is_int(task_id):
        return {
            "message": f"id {task_id} must be an integer", 
            "success": False 
        }, 400

    if request.method == "GET":
        if task:
            return task.to_json(), 200

    elif request.method == "PUT":
        if task: 
            task_data = request.get_json()
            task.title = task_data["title"]
            task.description = task_data["description"]
            db.session.commit()

            return make_response(f"Task #{task_id} successfully updated", 200)

    elif request.method == "DELETE":
        if task:
            db.session.delete(task)
            db.session.commit()
            return make_response(f"Task #{task_id} successfully deleted", 200)

    return make_response({
            "message": f"Task with {task_id} was not found", 
            "success": False 
        }, 404)

# @tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
# def single_task(task_id):
#     task = Task.query.get(task_id)
#     return make_response({
#         "task": {
#             "id": task.task_id,
#             "title": task.title,
#             "description": task.description,
#             "completed_at": task.task_completed()}
#         }, 200
#     )