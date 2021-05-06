from flask import current_app, Blueprint, make_response, jsonify, request
from app import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def post_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return make_response({
            "details": "Invalid data"
        }, 400)

    else: 
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])

        db.session.add(new_task)
        db.session.commit()

        return make_response({
            "task":{
                "id": new_task.id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": bool(new_task.completed_at)
            }
        }, 201)

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_all_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        })
    return make_response(jsonify(tasks_response), 200)

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_one_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)  #what is make_response and why needed only sometimes? 
    if request.method == "GET":
        return {"task":{
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }}, 200
    elif request.method == "PUT":
        form_data = request.get_json()  #what is form_data?
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()
        return make_response({"task":{
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }}, 200)
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({"details": f'Task {task.id} "{task.title}" successfully deleted'}), 200
