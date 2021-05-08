from app import db
from flask import Blueprint
from flask import request
from flask import jsonify, make_response
from .models.task import Task
from datetime import datetime

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#make a post request
@tasks_bp.route("", methods=["POST"])
def create_task():
    
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return make_response({"details": "Invalid data"}, 400) 
    task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])
    
    


    db.session.add(task)
    db.session.commit()

    return make_response(task.return_task_json(), 201)

#get requests
@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_tasks():
    tasks = Task.query.all()
    sort_query = request.args.get("sort")
    if sort_query:
        if 'asc' in sort_query:
            tasks = Task.query.order_by(Task.title.asc())
        elif 'desc' in sort_query:
            tasks = Task.query.order_by(Task.title.desc())
    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id" : task.task_id,
            "title" : task.title,
            "description": task.description,
            "is_complete":task.task_completed()
        })
    return jsonify(tasks_response), 200

@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def get_single_task(task_id):
    task = Task.query.get(task_id)
    form_data = request.get_json()
    if task is None:
        return make_response("", 404)
    if request.method == "GET":
        if task is None:
            return make_response("none", 404)
        return make_response(task.return_task_json())
    elif request.method == "PUT":        
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()
        return make_response(task.return_task_json())
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({"details": f'Task {task.task_id} "{task.title}" successfully deleted'}, 200)
    


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_task_complete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    task.completed_at = datetime.now()
    db.session.commit()
    return make_response(task.return_task_json(), 200)

@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def task_incomplete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404) 
    task.completed_at = None
    return make_response(task.return_task_json(), 200)