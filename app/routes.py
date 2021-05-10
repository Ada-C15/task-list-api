from app import db
from app.models.task import Task
# from app.models.goal import Goal
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime

tasks_bp = Blueprint(
    "tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    request_body = request.get_json()

    if "title" in request_body and "description" in request_body and "completed_at" in request_body:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body["completed_at"]
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"task": new_task.to_dict()}), 201

    else:
        return make_response({"details": "Invalid data"}, 400)


@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def task_index():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
    return make_response(jsonify(tasks_response), 200)


@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    if request.method == "GET":
        return jsonify({"task": task.to_dict()}), 200

    elif request.method == "PUT":
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data['description']
        task.completed_at = form_data["completed_at"]
        db.session.commit()

        return jsonify({"task": task.to_dict()}), 200

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        task_response = {
            "details": f'Task {task.task_id} "{task.title}" successfully deleted'}
        return make_response(task_response), 200


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"], strict_slashes=False)
def handle_complete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    else:
        task.completed_at = datetime.now()
        db.session.commit()
        return jsonify({"task": task.to_dict()}), 200


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"], strict_slashes=False)
def handle_incomplete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    else:
        task.completed_at = None
        db.session.commit()
        return jsonify({"task": task.to_dict()}), 200
