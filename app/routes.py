from app import db
from flask import Blueprint
from flask import request
from flask import jsonify, make_response
from .models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

#make a post request
@tasks_bp.route("", methods=["POST"])
def create_task():
    request_body = request.get_json()  
    task = Task(title=request_body["title"],
                    description=request_body["description"],
                    completed_at=request_body["completed_at"])

    db.session.add(task)
    db.session.commit()

    return make_response(task.return_task_json(), 201)

#get requests
@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_tasks():
    # if request.method == "GET":
    #     id_query = request.args.get("id")
    #     if id_query:
    #         tasks = Task.query.filter_by(id=id_query)
    tasks = Task.query.all()
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
    if task is None:
        return make_response("", 404)
    if request.method == "GET":
        if task is None:
            return make_response("none", 404)
        return make_response(task.return_task_json())
    elif request.method == "PUT":
        form_data = request.get_json()
        task.title = form_data["title"]
        task.description = form_data["description"]
        task.completed_at = form_data["completed_at"]
        db.session.commit()
        return make_response(task.return_task_json())
    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response(f"details", 200)

