from flask import Blueprint, request, jsonify
from werkzeug.wrappers import PlainRequest
from app import db
from flask.helpers import make_response
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

# come back and refactor into task_index & independent POST function
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

def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

# Handles GET requests for 1 method with the provided task id. 
@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_one_task(task_id):
    if not is_int(task_id):
        return{
            "message": f"ID {task_id} must be an integer",
            "success": False
        }, 400
    
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    else:
        return {
            "task": task.to_json()
        }, 200

@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):

    task = Task.query.get(task_id)

    if task:

        task_data = request.get_json()

        task.title = task_data["title"]
        task.description = task_data["description"]

        db.session.commit()

        return{
            "task": task.update_json()
        }, 200
    
    else:
        return make_response("", 404)

@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_task(task_id):

    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    else:
        db.session.delete(task)
        db.session.commit()

        return {
            "details": f'Task {task.task_id} "{task.title}" successfully deleted'
        }
