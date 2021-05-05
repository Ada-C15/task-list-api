from app import db
from app.models.task import Task
from flask import request, Blueprint, make_response
from flask import jsonify
from .models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

@tasks_bp.route("", methods=["POST"], strict_slashes=False)
def create_task():
    #Reads the HTTP request boby with:
    request_body = request.get_json()
    if len(request_body) == 3:
        new_task = Task(title = request_body["title"], description = request_body["description"], completed_at = None )
        
        db.session.add(new_task)
        db.session.commit()

        return {
            "task" : new_task.to_json()
        }, 201
        #return make_response(jsonify(new_task)), 201
    elif ("title" not in request_body) or ("description" not in request_body) or ("completed_at" not in request_body):
        response = {
            "details" : "Invalid data"
        }
        return make_response(response,400)


@tasks_bp.route("", methods=["GET"], strict_slashes=False)
def get_tasks():
    tasks = Task.query.all()
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_json())
    return jsonify(tasks_response), 200


@tasks_bp.route("/<task_id>", methods=["GET"], strict_slashes=False)
def get_one_task(task_id):
    if not isinstance(int(task_id), int):
        return {
            "message": f"ID {task_id} must be an integer",
            "success": False
        }, 400

    task = Task.query.get(task_id)
    if task:
        return{
            "task" : task.to_json()
        } , 200
    return make_response("",404)


@tasks_bp.route("/<task_id>",methods=["PUT"], strict_slashes=False)
def update_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return make_response("",404)

    updates_body = request.get_json()
    task.title = updates_body["title"]
    task.description = updates_body["description"]
    task.completed_at = updates_body["completed_at"]

    db.session.commit()

    return {
            "task" : task.to_json()
    }, 200

@tasks_bp.route("/<task_id>",methods=["DELETE"], strict_slashes=False)
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task == None:
        return make_response("",404)

    db.session.delete(task)
    db.session.commit()
    return {
        "details" : f"Task 1 \"{task.title}\" successfully deleted"
    }, 200