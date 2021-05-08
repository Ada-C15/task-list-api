from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response, jsonify
from datetime import datetime



tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.route("", methods = ["GET"])
def task_index():
    sort_query = request.args.get("sort")
    if sort_query == "asc":
        tasks = Task.query.order_by(Task.title.asc())
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
        
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    return jsonify(tasks_response), 200



@tasks_bp.route("", methods = ["POST"])
def tasks():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body or "completed_at" not in request_body:
        return make_response({ "details": "Invalid data"}, 400)
    else:  
        new_task = Task(title=request_body["title"],
                        description=request_body["description"],
                        completed_at=request_body["completed_at"])
        db.session.add(new_task)
        db.session.commit()
        return make_response(jsonify({"task": new_task.to_json()}), 201)

@tasks_bp.route("/<task_id>", methods = ["GET", "PUT", "DELETE"])
def handle_tasks(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    elif request.method == "GET":
        return {"task": task.to_json()}, 200
    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]

        db.session.commit()

        return { "task": task.to_json()}
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response({
            "details":f"Task {task.task_id} \"{task.title}\" successfully deleted"
        }, 200) 


@tasks_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    elif not task.is_complete(): 
        task.completed_at = True
    return {"task": task.to_json()}, 200
    
@tasks_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("", 404)
    elif task.is_complete(): 
        task.completed_at = None
    return {"task": task.to_json()}, 200









