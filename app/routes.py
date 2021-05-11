from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def handle_tasks():
    request_body = request.get_json()
    new_task = Task(title= request_body["title"],
    description= request_body["description"],
    completed_at= request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()

    return make_response(f"Task {new_task.title} has been created", 201)


@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def tasks_index():
    title_query = request.args.get("title")
    # if title_query:
    #     tasks = Task.query.filter_by(title=title_query)
    # else:
    tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.task_id,
            "title": task.title,
            "description": task.description,
            "completed_at": task.completed_at
        })
    return jsonify(tasks_response)


@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def handle_single_task(task_id):

    task = Task.query.get(task_id)

    if task is None:
            return make_response(f"Task {task_id} was not found.", 404)
    
    return {
        "id": task.task_id,
        "title": task.title,
        "description": task.description,
        "completed_at": task.completed_at
        }
    

@tasks_bp.route("/<task_id>", methods=["PUT"], strict_slashes=False)
def update_single_task(task_id):
    task = Task.query.get(task_id)

    request_body = request.get_json()

    if task is None:
            return make_response(f"Task {task_id} was not found.", 404)
    
    elif "title" not in request_body or "description" not in request_body:
        return {"message": "Request requires both a title and description."}, 400

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]

    db.session.commit()

    return make_response(f"Task #{task.task_id} successfully updated", 200)


@tasks_bp.route("/<task_id>", methods=["DELETE"], strict_slashes=False)
def delete_single_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
            return make_response(f"Task {task_id} was not found.", 404)
    
    db.session.delete(task)
    db.session.commit()

    return make_response(f"Task #{task.task_id} successfully deleted")

