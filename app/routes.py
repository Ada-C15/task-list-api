from app import db 
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify 
from datetime import datetime 
from sqlalchemy import desc, asc 

task_bp = Blueprint("tasks",__name__,url_prefix="/tasks")

@task_bp.route("", methods=["POST"])
def create_task():
    """Create a task for the database"""
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return make_response({"details": "Invalid data"}, 400)
    new_task = Task(title=request_body["title"], #value in db column == what user entered on their side
                    description=request_body["description"], 
                    completed_at=request_body["completed_at"])
    
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"task": new_task.to_json()}), 201

@task_bp.route("", methods=["GET"])
def get_all_tasks():
    """Get multiple tasks per request"""
    tasks_ordered = request.args.get("sort")

    if not tasks_ordered:
        tasks = Task.query.all()
    elif tasks_ordered == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif tasks_ordered == "desc":
        tasks = Task.query.order_by(desc(Task.title))

    hold_tasks = []
    if not tasks:
        return jsonify(hold_tasks) 

    for task in tasks:
        hold_tasks.append(task.to_json())
    return jsonify(hold_tasks)

@task_bp.route("/<task_id>", methods=["GET"])
def get_single_task(task_id):
    single_task = Task.query.get(task_id)

    if not single_task:
        return make_response("", 404)
    return jsonify({"task": single_task.to_json()})

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task_element(task_id):
    """Overwrites a task with details provided by the user"""
    task = Task.query.get(task_id)

    if not task:
        return make_response("", 404)

    request_body = request.get_json()
    # reassign user's changes to the corresponding db element
    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body["completed_at"]

    db.session.commit()
    return jsonify({"task": task.to_json()})

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return make_response("", 404)
    
    db.session.delete(task)
    db.session.commit()
    return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):

    task = Task.query.get(task_id)
    if not task:
        return make_response("", 404)
    # why no request body here? have one in PUT
    task.completed_at = datetime.now()
    db.session.commit()
    return jsonify({"task": task.to_json()})

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):

    task = Task.query.get(task_id)
    if not task:
        return make_response("", 404)
    # why no request body here? have one in PUT
    task.completed_at = None
    db.session.commit()
    return jsonify({"task": task.to_json()})

