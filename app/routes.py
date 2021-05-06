from app import db
from app.models.task import Task
from flask import Blueprint, make_response, request, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST", "GET"])
def handle_tasks():
    if request.method == "POST":
        request_body = request.get_json()

        new_task = Task(title=request_body['title'],
                        description=request_body['description'],
                        completed_at=request_body['completed_at'])

        db.session.add(new_task)
        db.session.commit()

        response = {
            "task": {
                "id": new_task.task_id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": is_task_complete(new_task)
            }
        }

        return make_response(jsonify(response), 201)

    elif request.method == "GET":

        tasks = Task.query.all()
        tasks_response = []

        for task in tasks:
            tasks_response.append({
                "id": task.task_id,
                "title": task.title,
                "descroption":task.description,
                "is_complete": is_task_complete(task)
            })

        return jsonify(tasks_response)

@tasks_bp.route("/<task_id>", methods=["GET", "PUT"])
def handle_task(task_id):
    
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)

    if request.method == "GET":
    
        return {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": is_task_complete(task)
            }
        }

    elif request.method == "PUT":

        request_body = request.get_json()

        task.title = request_body['title']
        task.description = request_body['description']
        task.completed_at = request_body['completed_at']

        db.session.commit()

        return {
            "task": {
                "id": task.task_id,
                "title": task.title,
                "description": task.description,
                "is_complete": is_task_complete(task)
            }
        }


# Helper functions
def is_task_complete(task):
    if not task.completed_at:
        return False
    return True