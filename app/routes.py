from flask import request, Blueprint, make_response
from app import db
from .models.task import Task
from flask import jsonify

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"])
def add_task():
    if request.content_type != 'application/json':
        return jsonify({"details": "Invalid data"}), 415

    request_body = request.get_json()
    title = request_body.get("title")
    description = request_body.get("description")
    completed_at = request_body.get("completed_at")

    if not title or not description or "completed_at" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    #   task_id=request_body["task_id"],
    new_task = Task(title=title,
                    description=description,
                    completed_at=completed_at)

    # print(new_task.title)
    # if not new_task.title:
    #     return jsonify({"details": "Invalid data"}), 400
    
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_json()}), 201


@tasks_bp.route("", methods=["GET"])
def get_task():
    tasks = Task.query.all()
    tasks_response = []

    for task in tasks:
        tasks_response.append(task.to_json())
        
    sort_response = []
    sort = request.args.get('sort')
    if sort == 'asc':
        ascend = Task.query.order_by(Task.title).all()
        for a in ascend:
            sort_response.append(a.to_json())
        return jsonify(sort_response), 200
    elif sort == 'desc':
        descend = Task.query.order_by(Task.title.desc()).all()
        for d in descend:
            sort_response.append(d.to_json())
        return jsonify(sort_response), 200

    return jsonify(tasks_response), 200


@tasks_bp.route("/<int:task_id>", methods=["GET"])
def get_single_task(task_id):
    # if not int(task_id):
    #     return make_response("", 404)
    
    task = Task.query.get(task_id)

    if task:
        return jsonify({"task": task.to_json()}), 200

    return make_response("", 404)


@tasks_bp.route("/<title>", methods=["GET"])


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


