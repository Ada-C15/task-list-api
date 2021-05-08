# 5/7/21, 1:48pm - waves 1,2 pass; last two wave-3 tests fail
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

    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body: 
        return make_response({"details": "Invalid data"}, 400)
    #else:
        # change date/time str to datetime obj so wave 3 tests can run 
        #dt_str = request_body["completed_at"]
        #if dt_str == None:
        #    request_body["completed_at"] = None
        # else:
        #     str_to_obj = datetime.datetime.strptime(dt_str, '%Y-%b-%d %H:%M:%S') # format of utcnow()
        #     request_body["completed_at"] = str_to_obj # bad practice in general!!!! - Jeremy

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

    tasks_ordered = request.args.get("sort")

    if not tasks_ordered:
        tasks = Task.query.all()
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
    """Overwrites a task with info provided by the user"""
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
        return ({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    """Updates a piece of a task's data with info provided by the user"""
    task = Task.query.get(task_id)

    if not task:
        return make_response("", 404)
    elif task:
        task.completed_at = datetime.datetime.now() # or utcnow() 
        db.session.commit()
        return jsonify({"task": task.to_json()}), 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_task_incomplete(task_id):
    """Updates a piece of a task's data with info provided by the user"""
    task = Task.query.get(task_id)

    if not task:
        return make_response("", 404)
    elif task:
        task.completed_at = None
        db.session.commit()
        return jsonify({"task": task.to_json()}), 200
