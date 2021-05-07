from app import db
from app.models.task import Task
from flask import Blueprint, jsonify, request, make_response
from sqlalchemy import desc, asc


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def tasks_index():
    sort_type = request.args.get("sort")

    if sort_type == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    elif sort_type == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    else:
        tasks = Task.query.all()
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())

    return jsonify(tasks_response), 200
    
@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_one_task(task_id):
    task = Task.query.get(task_id)
    
    if task == None:
        return make_response("", 404)

    return {
        "task": task.to_json()}, 200
        

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()
    try:
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])

    except KeyError:
        return make_response({
            "details": "Invalid data"
        }, 400)

    db.session.add(new_task)
    db.session.commit()

    return {
        "task": new_task.to_json()
    }, 201

@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    task = Task.query.get(task_id)
    form_data = request.get_json()

    if task == None:
        return make_response("", 404)
    
    task.title = form_data["title"]
    task.description = form_data["description"]
    task.is_complete = form_data["completed_at"]

    db.session.commit()

    return {
        "task": task.to_json()
    }, 200

@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return make_response("", 404)
    
    db.session.delete(task)
    db.session.commit()

    return make_response({
        "details": f'Task {task.task_id} "{task.title}" successfully deleted'
    })