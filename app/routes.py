from flask import Blueprint
from app.models.task import Task
from flask import Blueprint, make_response, jsonify, request
from app import db

task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")



@task_bp.route("", methods=["GET", "POST"])
def get_tasks():
    if request.method == "GET":
        tasks = Task.query.all()
        task_response = []

        for task in tasks:
            task_response.append({ "id": task.task_id, 
                                "title": task.title, 
                                "description": task.description, 
                                "is_complete": False})
        return jsonify(task_response), 200
    elif request.method == "POST":
        request_body = request.get_json()
        new_task = Task(title=request_body["title"], description=request_body["description"])
        db.session.add(new_task)
        db.session.commit()

        return make_response({"task": new_task.to_json()}, 201)

@task_bp.route("/<task_id>", methods=["GET"])
def get_single_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return make_response("", 404)
    else:
        return {"task": task.to_json()}

