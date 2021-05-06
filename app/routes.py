from flask import Blueprint
from app import db
from app.models.task import Task
from flask import jsonify
from flask import request, make_response
from datetime import datetime 


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def missing_data():
    return ({"details": "Invalid data"}, 400)


@tasks_bp.route("", methods=["POST"])
def handle_tasks():
    request_body = request.get_json()

    if not "title" in request_body or not request_body.get("title"): 
        return missing_data()
    if not "description" in request_body or not request_body.get("description"):
        return missing_data()
    if "completed_at" not in request_body:
        return missing_data()
    new_task = Task(title=request_body["title"], 
    description=request_body["description"], 
    completed_at=request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()
    return make_response({"task":new_task.to_json()}, 201)


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    title_query_sort = request.args.get("sort")
    if title_query_sort == "asc":
        tasks = Task.query.order_by(Task.title.asc()).all()    
    elif title_query_sort == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()
    else:        
        tasks = Task.query.all() 
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    return jsonify(tasks_response), 200 


def task_not_found(task_id):
    return make_response("", 404)


@tasks_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return ({"details": "Task 1 \"Go on my daily walk 🏞\" successfully deleted"}, 200) 
    return task_not_found(task_id)


@tasks_bp.route("/<task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return make_response({"task":task.to_json()}, 200)
    return task_not_found(task_id)


@tasks_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = Task.query.get(task_id)
    if task:
        new_data = request.get_json()
        task.title = new_data["title"]
        task.description = new_data["description"]
        task.completed_at = new_data["completed_at"]

        db.session.commit()
        return make_response({"task":task.to_json()}, 200)
    return task_not_found(task_id)


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def marking_complete(task_id):
    task = Task.query.get(task_id)
    if task:
        new_data = request.get_json()
        if task.completed_at == None:
            task.completed_at = datetime.today()
            db.session.commit()
        return make_response({"task":task.to_json()}, 200)
    return task_not_found(task_id)


@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"]) 
def marking_incomplete(task_id):
    task = Task.query.get(task_id)
    if task:
        new_data = request.get_json()
        if task.completed_at != None:
            task.completed_at = None 
            db.session.commit()
        return make_response({"task":task.to_json()}, 200)
    return task_not_found(task_id)