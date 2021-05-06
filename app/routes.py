from flask import request, Blueprint, make_response
from app import db
from .models.task import Task
from flask import jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def add_task():
    # if request.content_type != 'application/json':
    #     return jsonify({"details": "Invalid data"}), 415

    request_body = request.get_json()
    title = request_body.get("title")
    description = request_body.get("description")
    completed_at = request_body.get("completed_at")

    if not title or not description or "completed_at" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_task = Task(title=title,
                    description=description,
                    completed_at=completed_at)
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_json()}), 201


@tasks_bp.route("", methods=["GET"])
def get_task():
    tasks = Task.query.all()
    tasks_response = []

    sort = request.args.get("sort")
    if sort == "asc":
        tasks = Task.query.order_by(Task.title).all()
    elif sort == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()

    for task in tasks:
        tasks_response.append(task.to_json())

    return jsonify(tasks_response), 200


@tasks_bp.route("/<int:task_id>", methods=["GET"])
def get_single_task(task_id):
    # if not int(task_id):
    #     return make_response("", 404)
    task = Task.query.get(task_id)

    if task:
        return jsonify({"task": task.to_json()}), 200

    return make_response("", 404)


@tasks_bp.route("/<int:task_id>/mark_complete", methods=["PATCH"])
def update_completed_at(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    task.completed_at = True

    return jsonify({"task" :task.to_json()}), 200


@tasks_bp.route("/<int:task_id>/mark_incomplete", methods=["PATCH"])
def update_not_completed_at(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    task.completed_at = None

    return jsonify({"task" :task.to_json()}), 200



@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return jsonify({"task": task.to_json()}), 200

@tasks_bp.route("<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "details": f'Task {task_id} \"Go on my daily walk 🏞\" successfully deleted'
    })


