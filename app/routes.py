from app import db 
from flask import Blueprint
from flask import request
from flask import jsonify
from .models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["GET", "POST"])
def create_get_tasks():
    if request.method == "GET":
        tasks = Task.query.all()
        tasks_response = {}

        for task in tasks:
            tasks_response.append({
                "task_id": task.task_id,
                "title": task.title,
                "description": task.description,
                is_commplete: task.is_commplete
                })
        return jsonify(tasks_response), 201

    elif request.method == "POST":
        request_body = request.get_json()
        new_task = Task(title = request_body["title"],
                description = request_body["description"],
                completed_at = request_body["completed_at"])

    db.session.add(new_task)
    db.session.commit()
    
    return {
        "task": new_task.to_json()
        }, 201

# @tasks_bp.route("", methods=["POST"])
# def create_tasks():
#     request_body = request.get_json()
#     new_task = Task(title = request_body["title"],
#                 description = request_body["description"],
#                 completed_at = request_body["completed_at"])

#     db.session.add(new_task)
#     db.session.commit()
    
#     return {
#         "task": new_task.to_json()
#         }, 201

# @tasks_bp.route("", methods=["GET"])
# def get_tasks():
#     tasks = Task.query.all()
#     tasks_response = {}

#     for task in tasks:
#         tasks_response.append({
#         "id": task.id,
#         "title": task.title,
#         "description": task.description,
#         is_commplete: task.is_commplete
#         })
#         # tasks_response.append(task.to_json()) #using function for clean code 
#     return jsonify(tasks_response), 200

#GET PUT DELETE 
@tasks_bp.route("/<task_id>", methods=["GET", "PUT", "DELETE"])
def handle_task(task_id):
    task = Tasks.query.get(task_id)
    if task is None:
        return make_response("", 404)

    if request.method == "GET":
        return { "task": {
            "task_id": task.task_id,
            "title": task.title,
            "description": task.description,
            is_complete: task.is_complete
        }}

    elif request.method == "PUT":
        form_data = request.get_json()

        task.title = form_data["title"]
        task.description = form_data["description"]

        db.session.commit()
        return make_response("", 404)

    elif request.method == "DELETE":
        db.session.delete(task)
        db.session.commit()
        return make_response(f"Task #{task.id} successfully deleted")