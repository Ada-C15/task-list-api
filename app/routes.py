from app import db 
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify 
import datetime
from sqlalchemy import desc, asc

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks") 

@task_bp.route("", methods=["POST"])
def add_task():
    """Creates a task record and saves it to a database"""
    request_body = request.get_json()

    # bar incomplete entries
    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body: 
        return make_response({"details": "Invalid data"}, 400)
    else:
        new_task = Task(
            title=request_body["title"],
            description=request_body["description"],
            completed_at=request_body["completed_at"])

        db.session.add(new_task)
        db.session.commit()
        return jsonify({"task": new_task.to_json()}), 201

@task_bp.route("", methods=["GET"])
def get_tasks():
    """Retrieves tasks from the app's tasklist"""

    tasks_ordered = request.args.get("sort") # match given query param ...(here)

    if not tasks_ordered: # so if `/tasks?sort=asc` doesnt happen
        tasks = Task.query.all() # collection of Task objects
    elif tasks_ordered == "asc":
        tasks = Task.query.order_by(asc(Task.title))
    elif tasks_ordered == "desc":
        tasks = Task.query.order_by(desc(Task.title))

    task_collection = []
    if not tasks:
        return jsonify(task_collection)
    else: 
        for task in tasks:
            task_collection.append(task.to_json())
        return jsonify(task_collection)

@task_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    """Gets data of single task"""
    single_task = Task.query.get(task_id)

    if not single_task:
        return make_response("", 404)
    else:
        return jsonify({ "task": single_task.to_json() }), 200

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    """Updates a task with info provided by the user"""
    task = Task.query.get(task_id)
    
    if not task:
        return make_response("", 404)
    else:
        request_body = request.get_json()
        task.title = request_body["title"]
        task.description = request_body["description"]
        task.completed_at = request_body["completed_at"]
        db.session.commit()
        return jsonify({"task": task.to_json()}), 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Deletes a task from the task list"""
    task = Task.query.get(task_id)

    if not task:
        return make_response("", 404)
    else:
        db.session.delete(task)
        db.session.commit()
        return ({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}, 200) # formatting: match line 193 in wave_01.md

