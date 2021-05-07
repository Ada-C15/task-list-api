from app import db
from app.models.task import Task
from flask import Blueprint, request, jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods = ["POST"], strict_slashes = False)
def create_task():
    response_body = request.get_json()
    if len(response_body) < 3:
        return jsonify({"details": f'Invalid data'}), 400

    new_task = Task(title = response_body["title"],
                    description = response_body["description"],
                    completed_at = response_body["completed_at"])  

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.task_to_json()}), 201

@tasks_bp.route("", methods = ["GET"], strict_slashes = False)
def view_all_tasks():
    query_param_value = request.args.get("sort")
    if query_param_value == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    elif query_param_value == "asc":
        tasks = Task.query.order_by(Task.title).all()
    else:
        tasks = Task.query.all()

    tasks_view = []
    if tasks:
        for task in tasks:
            tasks_view.append(task.task_to_json())
    return jsonify(tasks_view)

@tasks_bp.route("/<task_id>", methods = ["GET"], strict_slashes = False)
def view_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify(None), 404
    return jsonify({"task": task.task_to_json()})

@tasks_bp.route("/<task_id>", methods = ["PUT"], strict_slashes = False)
def update_task(task_id):
    task = Task.query.get(task_id)
    updated_data = request.get_json()
    if not task or not updated_data:
        return jsonify(None), 404

    task.title = updated_data['title']
    task.description = updated_data["description"]
    task.completed_at = updated_data["completed_at"]

    db.session.commit()
    return jsonify({"task": task.task_to_json()})

@tasks_bp.route("/<task_id>", methods = ["DELETE"], strict_slashes = False)
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify(None), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"details": f'Task {task.task_id} "{task.title}" successfully deleted'})

    